# NEUS 642 Week 8: snapATAC2
The installation for this week's lesson is probably the hardest part. Give it a try at home before class, especially if you're working on Windows.

# For macOS/Linux
* Make sure you have the latest version of the course materials:
    * `cd your/path/to/NEUS642`
    * `git pull`

* (May not be necessary) Clone the environment configuration .yml
    * `git clone https://github.com/smlhkim/snapatac_setup`

* Create the new environment
`conda env create -n snapATAC2 -f notebooks/week08_02_23_ATACseq/util/snapATAC2.yml`
`conda activate snapATAC2`

* Open to this week's notebook
    * `jupyter lab`
    * notebooks > week08_02_23_ATACseq > Week8_ATACseq_inclass.ipynb

# For Windows
Installing in Windows is quite a bit more involved, as precompiled binaries are only available for macOS and x86_64 Linux systems. You're welcome to attempt building from source if you'd like, but installing Linux using the directions below will be much easier, and we were unable to ever get it to run on Windows. We've divided the process into two sections due to library version incompatibilities. Complete Section 1 before class, and we'll go through Section 2 after the first half of the lesson in class.

**Section 1**

* To begin, install WSL (Windows Subsystem for Linux), which allows users to run a native Linux environment directly on Windows without needing a virtual machine. This will mean coding in a Ubuntu terminal. Ubuntu is a free, open-source operating system (OS) based on Debian, which is based on the Linux kernel.
    * Open Terminal, PowerShell, or Command Prompt as administrator (e.g. right click the start button and select terminal (admin))
    * `wsl --install`
    * Restart your computer
    * WSL installation should come with Ubuntu. Open the start window and search for Ubuntu. A window should pop up and prompt you to create a username and password. Follow the prompts and then open up the ubuntu terminal.

* Install miniconda. Enter the following prompts into the terminal:
    * `sudo apt-get install wget`
    * `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
    * `bash Miniconda3-latest-Linux-x86_64.sh`
    * `source ~/.bashrc`

* Create a new environment
    * `conda create -n snapATAC2 python=3.10`
    * `conda activate snapATAC2`

* Make sure you have the latest version of the course materials. Linux has a slightly different file path nomenclature, so be aware of that!
    * `cd /mnt/c/…/…/…/NEUS642`
    * `git pull`

* Install snapATAC2 and other dependencies. You'll probably run into some errors due to dependency incompatibility, but you should still be able to get through the exercise.
    * `pip install snapatac2 jupyterlab umap-learn scanpy kaleido==0.2.1 git+https://github.com/KrishnaswamyLab/MAGIC.git#subdirectory=python`

* Open to this week's notebook
    * `jupyter lab`
    * Ctrl + click one of the URLs to open in browser
    * notebooks > week08_02_23_ATACseq > Week8_ATACseq_inclass.ipynb

**Section 2**

* End the Jupyter lab current session (ctrl + c)

* Install additional dependencies needed for annotation
    * `pip install scikit-misc scvi-tools`

* Re-open to this week's notebook and navigate back to where we left off
    * `jupyter lab`