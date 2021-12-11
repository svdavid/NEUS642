# NEUS 642 Week 1: Install Anaconda, Python and Jupyter Notebooks; Getting Started in Python

Our first class is independent and self-paced. It has two major components: 1) get python installed and running on your computer and 2) work through the Getting Started tutorial. For students with some Python experience, these exercises might be trivial. 

There are many ways to install Python. If you have already got Python and Jupter Notebooks installed and running on your computer, great!  However, anyone with limited experence should follow these steps and work through the exercises carefully, as they form a critical foundation for the rest of the class.

If you're very new to this and would like some more background, read this [overview of Python and the Jupyter Notebook programming environment](AboutPython.md). Then follow the directions below.

## Installing Anaconda

Traditionally, getting Python installed and working properly has required a fairly sophisiticated understanding of computers and programming. Happily, Anaconda is a community-driven software management system developed specifically as a user-friendly system for getting programming languages, including Python, up and running without having to puzzle over things like LIBPATHS and version conflicts. 

1. [Download and install Anaconda, following instructions specific to your operating system.](https://docs.anaconda.com/anaconda/install/index.html). You should be able to perform a standard installation.

2. [Run Jupyter Notebook](https://docs.anaconda.com/anaconda/user-guide/getting-started/). You should read through the entire Getting Started guide, but focus on the section "Run Python in a Jupyter Notebook". You might try Jupyer Lab, which is basically a fancier version of Notebook.


## Getting Started Tutorial

Now you need to copy down the materials from the course Github repository to your computer. To make it easy to get future updates to the notebooks, we are going to use Git, which is a source-code management tool. To get started, we will be using the command prompt. The command prompt is a program that allows you to interact with your computer using the keyboard instead of a mouse:

* Open `Anaconda Prompt`.
* Change to the directory where you want to store your files for NEUS642.
* Type `git clone https://github.com/svdavid/NEUS642`

If the last step fails, it means you need to install Git. While still in the `Anaconda Prompt`, type `conda install git`. Now, try the last step again. Once you have successfully run the last step, you will now have a folder called `NEUS642`. The next step is to make sure you have all the Python packages you need to run the code. In the `Anaconda Prompt`, type the following command:

```
conda install python matplotlib seaborn numpy pandas jupyter
```

You may not discover until later today that you are missing a package. If you discover this, just open up an `Anaconda Prompt` and run the above command.

Now, let's start Jupyter Notebook so we can see today's notebook. While still in the `Anaconda Prompt`:

* Change to the folder where you cloned the notebooks by typing `cd NEUS642`.
* Start Jupyter Notebook by typing `jupyter notebook`.

A web browser should immediately open and load Jupyter Notebook. Navigate to today's notebook (under `notebooks/2020/200107`) and open `Getting_Started_students.ipynb`. Now it's your turn to read the contents of the notebook and work through the exercises. Feel free to play around with the example code, add cells, etc. This is your sandbox!

Note that this is the "student" version of the notebook, which leaves the answers to exercises blank. If you need to get the solution, look in `Getting_Started_answers.ipynb`

## Notes on notebooks

You'll note that we have four versions of each notebook. The purpose of the other notebooks will become more clear during the in-class exercises. In case you're interested:

* `base` - This is the version you will create when authoring your own exercise. It contains all the answers to the exercises. The course staff has a script that will take this version and create three formatted versions of the notebook for use in the class. The formatted versions all contain a table of contents with links to easily navigate the notebook. Once you're ready to create the notebook for the class, the course staff will provide you instructions on how to properly format it so it works with the script.
* `students` - This is the version that you will use. The answers have been removed from the notebook so that you can enter your own solution.
* `teacher` - This is the version used by the presenter. The answers have been removed from the notebook, but will automatically be loaded once you execute the cell (note you will need to execute the cell twice, once to load the solution and again to run the solution).
* `answers` - Same as `base`, except it contains a nicely-formatted table of contents.

