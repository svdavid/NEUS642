This week's exercise requires some new packages that are not distributed on the main conda package channel. So to get them, you need to add a new source of packages before installing.

```
conda config --add channels conda-forge
conda install scikit-image 'aicsimageio[czi]' czifile
```