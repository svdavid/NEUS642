# NEUS 642 Week 1: Install Anaconda, Python and Jupyter Notebooks; Getting Started in Python

Our first class is independent and self-paced. It has two major components: 1) get Python installed and running on your computer and 2) work through the Getting Started tutorial. For students with some Python experience, these exercises might be easy. Good for you! Our goal is to make sure that everyone has the basics worked out before we launch into more focused problems.

To get started, everyone should read/review this [overview of Python and the Jupyter Notebook programming environment](AboutPython.md), and make sure you're familiar with some basic concepts. Then follow the directions below.

## Installing Anaconda Python

There are many ways to install Python. If you've already got Python and Jupyter Notebooks installed and running on your computer, that should be fine. However, if you don't have Python installed or aren't comfortable with managing a Python installation, you should follow these steps carefully, as they form a critical foundation for the rest of the class.

In the early days, getting Python installed and working properly required a fairly sophisiticated understanding of computers and programming. Happily, Anaconda is a community-driven software management system developed specifically as a user-friendly system for getting programming languages, including Python, up and running without having to puzzle over things like LIBPATHS and version conflicts. 

[Download and install Anaconda, following instructions specific to your operating system.](https://docs.anaconda.com/anaconda/install/index.html). You should be able to perform a standard installation. Once installed, you should be able to open the `Anaconda Navigator`. This provides a graphical interface for managing environments and packages, which you may find useful. [More info here](https://docs.anaconda.com/anaconda/user-guide/getting-started/). 

Graphical tools abound for managing packages and Git repositories, which you are welcome to explore. However, below we'll walk through a command-line approach to setting up Python, which generalizes well across different operating systems and doesn't rely on potentiall unstable quirks of different graphical tools.


## Configuring Python

The core components of Python are quite stripped down, and running analyses like those used in the course requires installation of packages.  We will use the `conda` package manager, which is built into Anaconda. To support the use of Python for many different applications, Anaconda allows the management of multiple virtual `environments`. These are independent configurations of Python, allowing different packages to be installed for different applications/projects. For simplicity, we'll lead you through setting up packages in the `base` environment, but you're welcome to explore and, for example, set up an environment specifically for NEUS642.

We will be using the command line terminal for configuration. The command-line terminal is a program that allows you to interact with your computer using the keyboard instead of a mouse:

* Open a command-line teriminal. The specifics depend on your operating system.
  * Windows: Open the `Anaconda Prompt`, which you can run from the Anaconda Navigator
  * MacOS/Linux: Open a standard system Terminal.
* Make sure you have all the Python packages you need for the first few lectures. Type the following command (several of these packages may already be installed, but this will just make sure that's the case):
```
conda install python matplotlib seaborn numpy pandas jupyterlab git
```
* In the future, you may need to install new packages, which can be done by running `conda install <PACKAGE-NAME>`


## Getting Started Tutorial

Now you need to download a copy of the materials from the course Github repository to your computer. To make it easy to get future updates to the notebooks, we are going to use Git, which is a source code management tool.

* Open a command-line teriminal, as described above.
* Create and/or change to the directory where you want to store your files for NEUS642, for example, `cd /Users/jane/class/` (For user "jane" who has created a "class" folder in his home directory. In Windows, this might look like `cd C:\Users\jane\class\`)
* Type `git clone https://github.com/svdavid/NEUS642`. (For this example, materials for the class will be downloaded to `/Users/jane/class/NEUS642/`)

If the last step fails, it means you need to install Git. While still in the terminal, type `conda install git`. Now, try the last step again. Once you have successfully run the last step, you will now have a folder called `/Users/jane/class/NEUS642`. 

Now, let's start Jupyter Notebook so we can see today's notebook. While still in the terminal:

* Change to the folder where you cloned the notebooks by typing `cd NEUS642`.
* Start Jupyter Notebook by typing `jupyter notebook`.

A web browser should immediately open and load Jupyter Notebook. Navigate to today's notebook (under `notebooks/week1_01-04_getting_started`) and open `Getting_Started.ipynb`. Now it's your turn to read the contents of the notebook and work through the exercises. Each exercise has includes special cell. If that cell is active, press "ctrl-enter" to load the answer and review your work. Also, feel free to play around with the example code, add cells, etc. This is your sandbox!


## Updating class materials

As the course progresses, we will be adding new materials to the NEUS Github repository. To update, you'll want to open a terminal and do the following:

* Change to the directory where store your files for NEUS642, for example, `cd /Users/jane/class/NEUS642`
* Type `git pull`. This should download any new files that have been created for upcoming meetings.


## Some notes on notebooks

You'll note that we have four versions of each notebook. The purpose of the other notebooks will become more clear during the in-class exercises. In case you're interested:

* `base` - This is the version you will create when authoring your own exercise. It contains all the answers to the exercises. The course staff has a script that will take this version and create three formatted versions of the notebook for use in the class. The formatted versions all contain a table of contents with links to easily navigate the notebook. Once you're ready to create the notebook for the class, the course staff will provide you instructions on how to properly format it so it works with the script.
* `students` - This is the version that you will use. The answers have been removed from the notebook so that you can enter your own solution.
* `teacher` - This is the version used by the presenter. The answers have been removed from the notebook, but will automatically be loaded once you execute the cell (note you will need to execute the cell twice, once to load the solution and again to run the solution).
* `answers` - Same as `base`, except it contains a nicely-formatted table of contents.

