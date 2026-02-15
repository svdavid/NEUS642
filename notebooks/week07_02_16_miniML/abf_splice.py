"""Utilities for converting ABF recordings into stitched HDF5 traces.

This module compiles the ABF loading/splicing helpers used in
`miniML exercise 1.ipynb` into an importable library.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pyabf
from scipy.ndimage import gaussian_filter1d, percentile_filter
from scipy.optimize import curve_fit


def abf_to_continuous(
    abf_path: str | Path,
    channel: int = 0,
    gap_s: float = 0.2,
    sweep_subset: Iterable[int] | None = None,
) -> tuple[np.ndarray, np.ndarray, list[float], str, float]:
    """Concatenate ABF sweeps into one continuous timebase.

    Parameters
    ----------
    abf_path
        Path to an ABF file.
    channel
        Channel index to load.
    gap_s
        Blank time inserted between sweeps.
    sweep_subset
        Optional iterable of sweep indices.

    Returns
    -------
    t_cont
        Continuous time array in seconds.
    y_cont
        Continuous signal array.
    boundaries
        Sweep-start timestamps in the continuous trace.
    units
        Y-axis units from the ABF metadata.
    sr
        Sampling rate in Hz.
    """
    abf = pyabf.ABF(str(abf_path))
    sr = float(abf.dataRate)
    units = str(getattr(abf, "sweepUnitsY", ""))

    sweeps = abf.sweepList if sweep_subset is None else list(sweep_subset)

    t_chunks: list[np.ndarray] = []
    y_chunks: list[np.ndarray] = []
    boundaries: list[float] = []

    t_cursor = 0.0
    for sweep in sweeps:
        abf.setSweep(sweepNumber=sweep, channel=channel)
        y = np.asarray(abf.sweepY, dtype=float)
        n = y.size

        t = t_cursor + np.arange(n, dtype=float) / sr
        boundaries.append(t_cursor)

        t_chunks.append(t)
        y_chunks.append(y)

        # Move cursor by sweep duration plus optional gap.
        t_cursor = float(t[-1]) + (1.0 / sr) + gap_s

    t_cont = np.concatenate(t_chunks) if t_chunks else np.array([], dtype=float)
    y_cont = np.concatenate(y_chunks) if y_chunks else np.array([], dtype=float)

    return t_cont, y_cont, boundaries, units, sr


def plot_abf_continuous(
    abf_path: str | Path,
    channel: int = 0,
    gap_s: float = 0.2,
    sweep_subset: Iterable[int] | None = None,
    show_boundaries: bool = True,
) -> None:
    """Plot ABF sweeps concatenated as a continuous trace."""
    t, y, boundaries, units, sr = abf_to_continuous(
        abf_path,
        channel=channel,
        gap_s=gap_s,
        sweep_subset=sweep_subset,
    )

    plt.figure(figsize=(14, 4))
    plt.plot(t, y, lw=0.6)
    plt.xlabel("Time (s)")
    plt.ylabel(f"Signal ({units})" if units else "Signal")
    plt.title(f"Continuous ABF (channel {channel}) | sr={sr:g} Hz | sweeps={len(boundaries)}")

    if show_boundaries and boundaries:
        for boundary in boundaries:
            plt.axvline(boundary, linewidth=0.6, alpha=0.4)

    plt.tight_layout()
    plt.show()


def _plateau_boundaries(cmd_q: np.ndarray) -> np.ndarray:
    """Return boundary indices (including 0 and N) where command changes."""
    change_idx = np.where(np.abs(np.diff(cmd_q)) > 0)[0] + 1
    return np.concatenate([[0], change_idx, [len(cmd_q)]])


def _mad(x: np.ndarray) -> float:
    """Median absolute deviation."""
    med = float(np.median(x))
    return float(np.median(np.abs(x - med)))


def _adaptive_trim_segment(
    seg: np.ndarray,
    sr: float,
    window_s: float = 0.004,
    tail_fraction: float = 0.5,
    level_k: float = 3.0,
    slope_k: float = 3.0,
    min_trim_s: float = 0.0,
    max_trim_s: float = 0.08,
    consecutive_windows: int = 3,
) -> tuple[np.ndarray, dict]:
    """Trim segment start until level and slope resemble settled baseline."""
    info = {"trim_n": 0, "trim_s": 0.0}
    n = len(seg)
    if n < 16:
        return seg, info

    w = max(int(window_s * sr), 3)
    tail_n = max(int(n * tail_fraction), 8)
    tail = seg[-tail_n:]
    baseline = float(np.median(tail))

    level_sigma = 1.4826 * _mad(tail)
    if level_sigma <= 0:
        level_sigma = float(np.std(tail))
    level_sigma = max(level_sigma, 1e-12)

    tail_diff = np.diff(tail)
    slope_sigma = 1.4826 * _mad(tail_diff) if tail_diff.size else 0.0
    if slope_sigma <= 0:
        slope_sigma = float(np.std(tail_diff)) if tail_diff.size else 0.0
    slope_sigma = max(slope_sigma, 1e-12)

    min_trim_n = max(int(min_trim_s * sr), 0)
    max_trim_n = min(int(max_trim_s * sr), n - w * consecutive_windows - 1)
    if max_trim_n <= min_trim_n:
        # If search range collapses, still enforce minimum trim when possible.
        trim_idx = min(min_trim_n, max(n - 1, 0))
        if trim_idx > 0:
            info["trim_n"] = int(trim_idx)
            info["trim_s"] = float(trim_idx / sr)
            return seg[trim_idx:], info
        return seg, info

    # Enforce minimum trim as fallback, even if no "settled" window is detected.
    trim_idx = int(min_trim_n)
    for start in range(min_trim_n, max_trim_n + 1):
        ok = True
        for j in range(consecutive_windows):
            a = start + j * w
            b = a + w
            if b > n:
                ok = False
                break
            win = seg[a:b]
            win_diff = np.diff(win)
            level_ok = abs(float(np.median(win)) - baseline) <= level_k * level_sigma
            if win_diff.size:
                slope_ok = float(np.percentile(np.abs(win_diff), 90)) <= slope_k * slope_sigma
            else:
                slope_ok = True
            if not (level_ok and slope_ok):
                ok = False
                break
        if ok:
            trim_idx = start
            break

    if trim_idx > 0:
        info["trim_n"] = int(trim_idx)
        info["trim_s"] = float(trim_idx / sr)
        return seg[trim_idx:], info
    return seg, info


def _exp_model(t: np.ndarray, amp: float, tau_s: float, offset: float) -> np.ndarray:
    return amp * np.exp(-t / tau_s) + offset


def _subtract_slow_baseline_decay(
    seg: np.ndarray,
    sr: float,
    baseline_win_s: float = 1.0,
    baseline_percentile: float = 80.0,
    baseline_smooth_s: float = 0.2,
    min_tau_s: float = 2.0,
    max_tau_s: float = 300.0,
    fit_downsample_hz: float = 200.0,
) -> tuple[np.ndarray, dict]:
    """Estimate and subtract slow exponential baseline decay over full segment."""
    info = {
        "slow_applied": False,
        "slow_amp": np.nan,
        "slow_tau_s": np.nan,
        "slow_offset": np.nan,
        "slow_fit_ds_factor": 1.0,
    }
    n = len(seg)
    if n < 64:
        return seg, info

    # Downsample first so percentile/smoothing run on shorter arrays.
    ds_factor = max(int(sr / max(fit_downsample_hz, 1.0)), 1)
    info["slow_fit_ds_factor"] = float(ds_factor)
    seg_ds = seg[::ds_factor]
    sr_ds = sr / ds_factor

    win = max(int(baseline_win_s * sr_ds), 5)
    if win % 2 == 0:
        win += 1
    base_env_ds = percentile_filter(seg_ds, percentile=float(baseline_percentile), size=win, mode="nearest")
    sigma = max(float(baseline_smooth_s) * sr_ds, 1.0)
    base_env_ds = gaussian_filter1d(base_env_ds, sigma=sigma)

    t_full = np.arange(n, dtype=float) / sr
    t_fit = np.arange(len(base_env_ds), dtype=float) / sr_ds
    y_fit = base_env_ds

    amp0 = float(y_fit[0] - y_fit[-1])
    off0 = float(y_fit[-1])
    tau0 = min(max((t_fit[-1] - t_fit[0]) / 3.0, min_tau_s), max_tau_s)
    try:
        popt, _ = curve_fit(
            _exp_model,
            t_fit,
            y_fit,
            p0=[amp0, tau0, off0],
            bounds=([-np.inf, min_tau_s, -np.inf], [np.inf, max_tau_s, np.inf]),
            maxfev=10000,
        )
        amp, tau_s, offset = map(float, popt)
        slow = _exp_model(t_full, amp, tau_s, offset)
    except Exception:
        # Fallback: subtract robust envelope when exponential fit fails.
        amp = np.nan
        tau_s = np.nan
        offset = np.nan
        slow = np.interp(t_full, t_fit, base_env_ds)

    corrected = seg - slow
    info["slow_applied"] = True
    info["slow_amp"] = amp
    info["slow_tau_s"] = tau_s
    info["slow_offset"] = offset
    return corrected, info


def _subtract_exponential_transient(
    seg: np.ndarray,
    sr: float,
    fit_s: float = 0.05,
    min_tau_s: float = 0.003,
    max_tau_s: float = 0.10,
    gain: float = 1.25,
    prefer_data_amp: bool = True,
    data_amp_window_s: float = 0.002,
) -> tuple[np.ndarray, dict]:
    """Fit and subtract an initial exponential transient. Optional, use with care."""
    info = {
        "exp_applied": False,
        "exp_amp": np.nan,
        "exp_tau_s": np.nan,
        "exp_offset": np.nan,
        "exp_gain": gain,
    }
    n = len(seg)
    fit_n = min(n, max(int(fit_s * sr), 24))
    if fit_n < 24:
        return seg, info

    t = np.arange(fit_n, dtype=float) / sr
    y = seg[:fit_n]
    baseline = float(np.median(seg[max(fit_n // 2, 0) :]))
    amp0 = float(y[0] - baseline)
    if abs(amp0) < 1e-12:
        return seg, info

    min_tau_s = max(float(min_tau_s), 1.0 / sr)
    tau0 = min(max(fit_s / 4.0, min_tau_s), max_tau_s)
    try:
        popt, _ = curve_fit(
            _exp_model,
            t,
            y,
            p0=[amp0, tau0, baseline],
            bounds=([-np.inf, min_tau_s, -np.inf], [np.inf, max_tau_s, np.inf]),
            maxfev=5000,
        )
    except Exception:
        return seg, info

    amp, tau_s, offset = map(float, popt)
    if prefer_data_amp:
        amp_n = max(int(data_amp_window_s * sr), 3)
        data_amp = float(np.median(seg[:amp_n]) - baseline)
        if abs(data_amp) > abs(amp):
            amp = data_amp

    full_t = np.arange(n, dtype=float) / sr
    transient = gain * (_exp_model(full_t, amp, tau_s, offset) - offset)
    corrected = seg - transient

    info["exp_applied"] = True
    info["exp_amp"] = amp
    info["exp_tau_s"] = tau_s
    info["exp_offset"] = offset
    return corrected, info


def extract_segments_across_sweeps(
    abf_path: str | Path,
    channel: int = 0,
    target_cmd: float = -70.0,
    cmd_tol: float = 0.5,
    cmd_quant: float = 0.05,
    edge_buffer_s: float = 0.03,
    min_len_s: float = 0.10,
    baseline_method: str = "median",
    transient_correction: str = "none",
    adaptive_window_s: float = 0.004,
    adaptive_tail_fraction: float = 0.5,
    adaptive_level_k: float = 3.0,
    adaptive_slope_k: float = 3.0,
    adaptive_min_trim_s: float = 0.0,
    adaptive_max_trim_s: float = 0.08,
    adaptive_consecutive_windows: int = 3,
    exp_fit_s: float = 0.05,
    exp_min_tau_s: float = 0.003,
    exp_max_tau_s: float = 0.10,
    exp_gain: float = 1.25,
    exp_prefer_data_amp: bool = True,
    exp_data_amp_window_s: float = 0.002,
    slow_baseline_correction: str = "none",
    slow_baseline_win_s: float = 1.0,
    slow_baseline_percentile: float = 80.0,
    slow_baseline_smooth_s: float = 0.2,
    slow_exp_min_tau_s: float = 2.0,
    slow_exp_max_tau_s: float = 300.0,
    slow_fit_downsample_hz: float = 200.0,
) -> tuple[list[np.ndarray], dict]:
    """Extract baseline-corrected command-matched segments across all sweeps.

    `target_cmd`/`cmd_tol` use the units of `abf.sweepC` (e.g., mV in VC mode).
    `transient_correction` can be:
    - `none`
    - `adaptive_trim`
    - `exp_subtract`
    - `adaptive_trim+exp_subtract`
    """
    if baseline_method not in {"median", "mean"}:
        raise ValueError("baseline_method must be 'median' or 'mean'")
    valid_corrections = {"none", "adaptive_trim", "exp_subtract", "adaptive_trim+exp_subtract"}
    if transient_correction not in valid_corrections:
        raise ValueError(f"transient_correction must be one of {sorted(valid_corrections)}")
    valid_slow = {"none", "exp_decay"}
    if slow_baseline_correction not in valid_slow:
        raise ValueError(f"slow_baseline_correction must be one of {sorted(valid_slow)}")

    abf = pyabf.ABF(str(abf_path))
    sr = float(abf.dataRate)
    units = None

    seg_table: list[dict] = []
    segments: list[np.ndarray] = []

    for sweep in abf.sweepList:
        abf.setSweep(sweepNumber=sweep, channel=channel)
        y = np.asarray(abf.sweepY, dtype=np.float32)
        cmd = abf.sweepC

        if cmd is None:
            raise ValueError("No command waveform found (abf.sweepC is None).")

        cmd = np.asarray(cmd, dtype=np.float32)

        if units is None:
            units = str(getattr(abf, "sweepUnitsY", ""))

        cmd_q = np.round(cmd / cmd_quant) * cmd_quant if cmd_quant > 0 else cmd
        bounds = _plateau_boundaries(cmd_q)
        buf_n = max(int(round(edge_buffer_s * sr)), 0)
        min_len_n = max(int(round(min_len_s * sr)), 1)

        for a, b in zip(bounds[:-1], bounds[1:]):
            cmd_val = float(cmd_q[a])
            if abs(cmd_val - target_cmd) > cmd_tol:
                continue

            # Slice by indices (faster than building boolean masks over entire sweep).
            start_idx = int(a) + buf_n
            end_idx = int(b) - buf_n  # exclusive
            if end_idx <= start_idx:
                continue
            if (end_idx - start_idx) < min_len_n:
                continue

            seg = y[start_idx:end_idx]
            if seg.size == 0:
                continue
            t0 = float(start_idx / sr)
            t1 = float((end_idx - 1) / sr)

            seg_work = seg
            trim_info = {"trim_n": 0, "trim_s": 0.0}
            exp_info = {
                "exp_applied": False,
                "exp_amp": np.nan,
                "exp_tau_s": np.nan,
                "exp_offset": np.nan,
            }
            slow_info = {
                "slow_applied": False,
                "slow_amp": np.nan,
                "slow_tau_s": np.nan,
                "slow_offset": np.nan,
            }

            if "adaptive_trim" in transient_correction:
                seg_work, trim_info = _adaptive_trim_segment(
                    seg_work,
                    sr=sr,
                    window_s=adaptive_window_s,
                    tail_fraction=adaptive_tail_fraction,
                    level_k=adaptive_level_k,
                    slope_k=adaptive_slope_k,
                    min_trim_s=adaptive_min_trim_s,
                    max_trim_s=adaptive_max_trim_s,
                    consecutive_windows=adaptive_consecutive_windows,
                )

            if seg_work.size < max(int(min_len_s * sr), 8):
                continue

            if "exp_subtract" in transient_correction:
                seg_work, exp_info = _subtract_exponential_transient(
                    seg_work,
                    sr=sr,
                    fit_s=exp_fit_s,
                    min_tau_s=exp_min_tau_s,
                    max_tau_s=exp_max_tau_s,
                    gain=exp_gain,
                    prefer_data_amp=exp_prefer_data_amp,
                    data_amp_window_s=exp_data_amp_window_s,
                )

            if slow_baseline_correction == "exp_decay":
                seg_work, slow_info = _subtract_slow_baseline_decay(
                    seg_work,
                    sr=sr,
                    baseline_win_s=slow_baseline_win_s,
                    baseline_percentile=slow_baseline_percentile,
                    baseline_smooth_s=slow_baseline_smooth_s,
                    min_tau_s=slow_exp_min_tau_s,
                    max_tau_s=slow_exp_max_tau_s,
                    fit_downsample_hz=slow_fit_downsample_hz,
                )

            offset = float(np.median(seg_work) if baseline_method == "median" else np.mean(seg_work))
            seg_corr = seg_work - offset

            segments.append(seg_corr)
            seg_table.append(
                {
                    "sweep": int(sweep),
                    "cmd": cmd_val,
                    "t0_s": t0,
                    "t1_s": t1,
                    "dur_s": float(t1 - t0),
                    "n_samples": int(seg_corr.size),
                    "baseline_offset": offset,
                    "trim_n": trim_info["trim_n"],
                    "trim_s": trim_info["trim_s"],
                    "exp_applied": exp_info["exp_applied"],
                    "exp_amp": exp_info["exp_amp"],
                    "exp_tau_s": exp_info["exp_tau_s"],
                    "exp_offset": exp_info["exp_offset"],
                    "exp_gain": exp_info.get("exp_gain", exp_gain),
                    "slow_applied": slow_info["slow_applied"],
                    "slow_amp": slow_info["slow_amp"],
                    "slow_tau_s": slow_info["slow_tau_s"],
                    "slow_offset": slow_info["slow_offset"],
                    "slow_fit_ds_factor": slow_info.get("slow_fit_ds_factor", np.nan),
                }
            )

    if not segments:
        raise ValueError(
            "No segments found. Try:\n"
            "- increase cmd_tol\n"
            "- decrease edge_buffer_s / min_len_s\n"
            "- decrease cmd_quant (e.g., 0.01)\n"
            "- confirm target_cmd units/value"
        )

    meta = {
        "sample_rate_hz": sr,
        "units": units,
        "target_cmd": target_cmd,
        "cmd_tol": cmd_tol,
        "cmd_quant": cmd_quant,
        "edge_buffer_s": edge_buffer_s,
        "min_len_s": min_len_s,
        "baseline_method": baseline_method,
        "transient_correction": transient_correction,
        "adaptive_window_s": adaptive_window_s,
        "adaptive_tail_fraction": adaptive_tail_fraction,
        "adaptive_level_k": adaptive_level_k,
        "adaptive_slope_k": adaptive_slope_k,
        "adaptive_min_trim_s": adaptive_min_trim_s,
        "adaptive_max_trim_s": adaptive_max_trim_s,
        "adaptive_consecutive_windows": adaptive_consecutive_windows,
        "exp_fit_s": exp_fit_s,
        "exp_min_tau_s": exp_min_tau_s,
        "exp_max_tau_s": exp_max_tau_s,
        "exp_gain": exp_gain,
        "exp_prefer_data_amp": exp_prefer_data_amp,
        "exp_data_amp_window_s": exp_data_amp_window_s,
        "slow_baseline_correction": slow_baseline_correction,
        "slow_baseline_win_s": slow_baseline_win_s,
        "slow_baseline_percentile": slow_baseline_percentile,
        "slow_baseline_smooth_s": slow_baseline_smooth_s,
        "slow_exp_min_tau_s": slow_exp_min_tau_s,
        "slow_exp_max_tau_s": slow_exp_max_tau_s,
        "slow_fit_downsample_hz": slow_fit_downsample_hz,
        "segment_table": seg_table,
    }
    return segments, meta


def stitch_segments(segments: list[np.ndarray], sr: float) -> tuple[np.ndarray, np.ndarray]:
    """Concatenate extracted segments into one stitched trace."""
    y = np.concatenate(segments)
    t = np.arange(len(y), dtype=float) / float(sr)
    return t, y


def detrend_linear(t: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Remove linear drift from a stitched trace."""
    coeff = np.polyfit(t, y, 1)
    return y - np.polyval(coeff, t)


def plot_segment_diagnostics(
    segments: list[np.ndarray],
    meta: dict,
    max_segments: int = 6,
    show_legend: bool = False,
) -> None:
    """Overlay a subset of extracted segments for quick QC."""
    sr = float(meta["sample_rate_hz"])
    table = meta["segment_table"]

    plt.figure(figsize=(12, 4))
    for i, seg in enumerate(segments[:max_segments]):
        tt = np.arange(len(seg), dtype=float) / sr
        plt.plot(tt, seg, lw=0.8, label=f"seg {i} (sweep {table[i]['sweep']})")

    plt.xlabel("Time (s)")
    plt.ylabel(f"Signal ({meta['units']})" if meta.get("units") else "Signal")
    plt.title(f"First {min(max_segments, len(segments))} segments (baseline-corrected)")
    if show_legend:
        plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()


def save_stitched_h5(
    output_path: str | Path,
    t_stitched: np.ndarray,
    y_stitched: np.ndarray,
    meta: dict,
) -> Path:
    """Save stitched trace plus extraction metadata to HDF5.

    Datasets
    --------
    - `mini_data` (miniML-compatible trace dataset)
    - `segment_table` columns:
      `[sweep, cmd, t0_s, t1_s, dur_s, n_samples, baseline_offset]`
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with h5py.File(output, "w") as handle:
        # miniML's MiniTrace.from_h5_file() defaults to tracename='mini_data'.
        handle.create_dataset("mini_data", data=y_stitched)
        handle.attrs["sampling_interval_s"] = 1.0 / float(meta["sample_rate_hz"])
        handle.attrs["sample_rate_hz"] = meta["sample_rate_hz"]
        handle.attrs["units"] = meta["units"]
        handle.attrs["target_cmd"] = meta["target_cmd"]
        handle.attrs["cmd_tol"] = meta["cmd_tol"]
        handle.attrs["cmd_quant"] = meta["cmd_quant"]
        handle.attrs["edge_buffer_s"] = meta["edge_buffer_s"]
        handle.attrs["min_len_s"] = meta["min_len_s"]
        handle.attrs["baseline_method"] = meta["baseline_method"]
        handle.attrs["transient_correction"] = meta.get("transient_correction", "none")
        handle.attrs["exp_fit_s"] = meta.get("exp_fit_s", np.nan)
        handle.attrs["exp_min_tau_s"] = meta.get("exp_min_tau_s", np.nan)
        handle.attrs["exp_max_tau_s"] = meta.get("exp_max_tau_s", np.nan)
        handle.attrs["exp_gain"] = meta.get("exp_gain", np.nan)
        handle.attrs["slow_baseline_correction"] = meta.get("slow_baseline_correction", "none")
        handle.attrs["slow_baseline_win_s"] = meta.get("slow_baseline_win_s", np.nan)
        handle.attrs["slow_baseline_percentile"] = meta.get("slow_baseline_percentile", np.nan)
        handle.attrs["slow_baseline_smooth_s"] = meta.get("slow_baseline_smooth_s", np.nan)
        handle.attrs["slow_exp_min_tau_s"] = meta.get("slow_exp_min_tau_s", np.nan)
        handle.attrs["slow_exp_max_tau_s"] = meta.get("slow_exp_max_tau_s", np.nan)
        handle.attrs["slow_fit_downsample_hz"] = meta.get("slow_fit_downsample_hz", np.nan)

        seg_arr = np.array(
            [
                (
                    row["sweep"],
                    row["cmd"],
                    row["t0_s"],
                    row["t1_s"],
                    row["dur_s"],
                    row["n_samples"],
                    row["baseline_offset"],
                )
                for row in meta["segment_table"]
            ],
            dtype=float,
        )
        handle.create_dataset("segment_table", data=seg_arr)

        seg_corr = np.array(
            [
                (
                    row.get("trim_n", 0),
                    row.get("trim_s", 0.0),
                    1.0 if row.get("exp_applied", False) else 0.0,
                    row.get("exp_amp", np.nan),
                    row.get("exp_tau_s", np.nan),
                    row.get("exp_offset", np.nan),
                    row.get("exp_gain", np.nan),
                    1.0 if row.get("slow_applied", False) else 0.0,
                    row.get("slow_amp", np.nan),
                    row.get("slow_tau_s", np.nan),
                    row.get("slow_offset", np.nan),
                    row.get("slow_fit_ds_factor", np.nan),
                )
                for row in meta["segment_table"]
            ],
            dtype=float,
        )
        handle.create_dataset("segment_correction", data=seg_corr)

    return output


def default_stitched_h5_path(abf_path: str | Path, target_cmd: float) -> Path:
    """Return the notebook-style output path for stitched H5 files."""
    base = Path(abf_path).with_suffix("")
    return Path(f"{base}_cmd{target_cmd:g}_stitched.h5")


def run_abf_stitch_pipeline(
    abf_path: str | Path,
    channel: int = 0,
    target_cmd: float = 30.0,
    cmd_tol: float = 0.5,
    cmd_quant: float = 0.05,
    edge_buffer_s: float = 0.03,
    min_len_s: float = 0.10,
    baseline_method: str = "median",
    transient_correction: str = "adaptive_trim",
    adaptive_window_s: float = 0.004,
    adaptive_tail_fraction: float = 0.5,
    adaptive_level_k: float = 3.0,
    adaptive_slope_k: float = 3.0,
    adaptive_min_trim_s: float = 0.0,
    adaptive_max_trim_s: float = 0.08,
    adaptive_consecutive_windows: int = 3,
    slow_baseline_correction: str = "exp_decay",
    slow_baseline_win_s: float = 1.0,
    slow_baseline_percentile: float = 80.0,
    slow_baseline_smooth_s: float = 0.2,
    slow_exp_min_tau_s: float = 2.0,
    slow_exp_max_tau_s: float = 300.0,
    slow_fit_downsample_hz: float = 200.0,
    detrend: bool = True,
    output_path: str | Path | None = None,
) -> Path:
    """End-to-end helper to extract, stitch, optionally detrend, and save H5."""
    if transient_correction == "exp_subtract" or transient_correction == "adaptive_trim+exp_subtract":
        raise ValueError(
            "run_abf_stitch_pipeline no longer supports exp_subtract. "
            "Use transient_correction='none' or 'adaptive_trim', or call "
            "extract_segments_across_sweeps directly for exp_subtract."
        )
    segments, meta = extract_segments_across_sweeps(
        abf_path=abf_path,
        channel=channel,
        target_cmd=target_cmd,
        cmd_tol=cmd_tol,
        cmd_quant=cmd_quant,
        edge_buffer_s=edge_buffer_s,
        min_len_s=min_len_s,
        baseline_method=baseline_method,
        transient_correction=transient_correction,
        adaptive_window_s=adaptive_window_s,
        adaptive_tail_fraction=adaptive_tail_fraction,
        adaptive_level_k=adaptive_level_k,
        adaptive_slope_k=adaptive_slope_k,
        adaptive_min_trim_s=adaptive_min_trim_s,
        adaptive_max_trim_s=adaptive_max_trim_s,
        adaptive_consecutive_windows=adaptive_consecutive_windows,
        slow_baseline_correction=slow_baseline_correction,
        slow_baseline_win_s=slow_baseline_win_s,
        slow_baseline_percentile=slow_baseline_percentile,
        slow_baseline_smooth_s=slow_baseline_smooth_s,
        slow_exp_min_tau_s=slow_exp_min_tau_s,
        slow_exp_max_tau_s=slow_exp_max_tau_s,
        slow_fit_downsample_hz=slow_fit_downsample_hz,
    )

    t_stitched, y_stitched = stitch_segments(segments, meta["sample_rate_hz"])
    if detrend:
        y_stitched = detrend_linear(t_stitched, y_stitched)

    final_output = Path(output_path) if output_path else default_stitched_h5_path(abf_path, target_cmd)
    return save_stitched_h5(final_output, t_stitched, y_stitched, meta)


__all__ = [
    "abf_to_continuous",
    "plot_abf_continuous",
    "extract_segments_across_sweeps",
    "stitch_segments",
    "detrend_linear",
    "plot_segment_diagnostics",
    "save_stitched_h5",
    "default_stitched_h5_path",
    "run_abf_stitch_pipeline",
]
