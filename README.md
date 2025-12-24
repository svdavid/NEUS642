# NEUS 642: Python Programming in Neuroscience

<!-- vim-markdown-toc GFM -->

* [Overview](#overview)
* [Time and location](#time-and-location)
* [Course staff](#course-staff)
* [Preparing for the course](#preparing-for-the-course)
* [Schedule](#schedule)
* [Assessment](#assessment)
	* [Grading](#grading)
	* [Developing an exercise](#developing-an-exercise)
* [Python](#python)
	* [Python server](#python-server)
	* [Installing Python](#installing-python)
	* [Code editors](#code-editors)
	* [Course-specific resources](#course-specific-resources)
	* [Other resources](#other-resources)

<!-- vim-markdown-toc -->

## Overview
NEUS 642 is a hands-on course on the basics of Python programming for analysis of neuroscience-related data. A basic knowledge of programming is encouraged, but the course is open to students of ALL levels of programming experience. By the end of the course, students will have learned basic programming tasks, including loading and manipulating data sets, signal processing, image processing, and plotting. The course will be highly interactive. Students (with the support of TAs and instructors) will be expected to design and lead exercises during the class, and they are strongly encouraged to bring their own data and/or analysis problem to the course.

Before each meeting, students will be expected to work through a series of guided exercises in a Jupyter Notebook, a documents that contain live code, equations, visualizations and narrative text. During each meeting, we will review that work and work interactively on a small project that builds on the previous week's exercises. 

It is expected that each student can bring their own laptop. If you don't have a laptop, contact the instructors, and we can arrange a loan. During the first meeting, we will go through the specifics of setting up JupyterLab. But if you want to get a head start, learn more from our [Jupyter cheat sheet](cheatsheet.md).

The unique student-led approach used in this class was developed initially for the 2018 OHSU [Python Neurobootcamp](https://github.com/dasaderi/python_neurobootcamp). Thanks to the bootcamp organizers, Daniela Saderi, Brad Buran, Ted Laderdas, and Lisa Karstens, as well as the enthusiastic bootcamp participants for the ideas and effort that have made this course possible.     

## Time and location
* Time: Tuesdays 1-3pm during the winter quarter (January 9 through March 19, 2024).
* Location: Vollum M1441. (If there is strong interest, we will look into remote/hybrid access.)

## Course staff
### Course director:
* *Stephen David, Ph.D.*. Associate Professor, Oregon Hearing Research Center (davids@ohsu.edu).

### Teaching assistant(s):
* *Jonah Stickney*. Ph.D. Student, Behavioral and Systems Neuroscience

## Preparing for the course
Before our first meeting, please do the following:

* Sign up for our [NEUS642 Slack workspace](https://neus642.slack.com). If you haven't already received the invite, please contact one of the course staff for assistance.

* Find a laptop you can bring to class. Each class will have an interactive, hands-on exercise developed by you or one of your classmates. You'll be working on the exercise using your laptop.

* If you're not already familiar with Python, please start learning Python 3. You can work through the [suggested online courses and/or read the eBook](#python). 

* Think about a dataset that you would like to work on for the class. During the course, you will be asked to develop an exercise based on this dataset (either individually or in a small group of two or three). Some ideas for projects:
  * Complete a multivariate regression on your data using the `statsmodels` library
  * Use `biopython` to complete a BLAST query.
  * Generate a simple `SQLite` database to keep track of your experiments.
  * Align a set of images using `opencv-python`
  
## Schedule

The first four weeks are designed to lead students through the basics of working with data in Python and will consist of material and exercises designed by the instructors. These lectures will also model the notebook-based format for student-led that will make up the remainder of the course. Each subsequent meeting, a student or group of students will lead the class through a notebook highlighting an analysis they developed to tackle a specific analysis problem.  

* Week 1 (Jan 9): [Installing Anaconda and Python basics](notebooks/week1_01-04_getting_started/README.md)
* Week 2 (Jan 16): [Getting started with numerical analysis](notebooks/week2_01-11_numpy/README.md)
* Week 3 (Jan 23): [Working with dataframes](notebooks/week3_01-18_pandas/README.md)
* Week 4 (Jan 30): [Image processing basics](notebooks/week4_01-25_images/README.md)
* Weeks 5-11: Student-lead presentations

## Assessment

### Grading
This is a pass/no pass course worth three credits. Grading will be based on the following:
* Class attendance and participation in discussions
* Preparation of an exercise for at least one session

### Developing an exercise
All exercises will follow the format established in the original OHSU Python Neurobootcamp and previous years' meetings of NEUS 642. Notebooks from these previous iterations of the course are available in the [notebook archive](https://github.com/svdavid/NEUS642/tree/master/notebooks/archive) of the current course repository.

Material for this course will be made freely available as a learning resource for future scientists, both at OHSU and elsewhere. Therefore, we ask that all datasets and materials be licensed under a [Creative Commons](https://creativecommons.org) license and the [BSD license](https://opensource.org/licenses/BSD-3-Clause).

You'll be asked to develop a 90-minute exercise based on a dataset you'd like to work with. This dataset can be from your own work or obtained from a lab. The exercise will be formatted as a Jupyter Notebook and uploaded to the [NEUS642 webpage](https://github.com/svdavid/NEUS642) prior to the start of class. If you require additional third-party packages for running the exercise, please check with the course instructors so that instructions for installing the packages can be provided to students in advance.

All exercises must contain sufficient background to the problem that gives your classmates sufficient background to understand the problem. Your classmates are neuroscientists, but will need some additional, domain-specific knowledge to understand the problem. Do not skip this step, or you will lose your classmates!     

First, identify a dataset you'd like to work with. If you need help identifying a dataset pertinent to your area of interest, please contact a TA or course instructor. The dataset should be of reasonable size (i.e., no 10 gigabyte confocal images). You may need to do some post-processing of the data to get the file down to a reasonable size.    

Next, think of a reasonable problem that you can walk the class through in two hours. The exercise should load the data, perform some processing and/or summary of the data and then plot the results.   

Now, write the code to perform these steps and generate your plot. Once the code works, break it down into individual cells for a Jupyter Notebook. Above each code cell, add a Markdown cell explaining what's happening in the block below. Identify four or five cells that may serve as exercises. You'll remove the code from these cells and add some explanation above the blank cell instructing the class what problem needs to be solved before they can move onto the next step. They will then have 5-15 minutes (depending on the complexity of the problem) to try and figure out the code that solves the problem.        

Throughout the development process, you will be expected to consult with the TAs and course organizers to ensure that your exercise is of appropriate level and scope for the class. It's better to be a little short than to go over time!  

We've compiled some additional [guidelines](guidelines.md), which are useful to review as you prepare your exercise. 

## Python
Students are expected to have a basic knowledge of programming. If you haven't worked with Python before, please take an online introductory course prior to the start of class such as those offered by [codecademy](https://www.codecademy.com/learn/learn-python-3) and [udacity](https://www.udacity.com/course/intro-to-computer-science--cs101). [A Byte of Python](https://python.swaroopch.com/) is a free eBook; however, you will need your own copy of Python to run and test the code.      

We will be using Python 3.7 or later for the course. The changes in newer versions of Python are relatively small. The last major overhaul was version 3.0. Some widely used code still runs on 2.0, but that should not be relevant to most of you.

You may wish to work through the five days of the [Python NeuroBootcamp](https://github.com/dasaderi/python_neurobootcamp). You can [download](https://github.com/dasaderi/python_neurobootcamp/archive/master.zip) the notebooks to your computer and run them using Jupyter Lab (see below). If you have any trouble or questions, you can post them to the Slack channel. As a bonus, you may work through the notebooks from the [winter 2020 iteration of NEUS642](https://github.com/svdavid/NEUS642/tree/master/notebooks/archive/2020). We will be working through some of these notebooks during the first few weeks of class.

### Installing Python
We recommend the [Anaconda Python Distribution](https://www.anaconda.com), since it is free to use (both for commercial and academic use) and makes it easy to install a huge variety of third-party Python packages. To get started with your own copy of Python::  

* [Download](https://www.anaconda.com/download) the installer and run it. Select all default options. When it asks you whom to install for, select "Just Me" (the recommended option). You can skip the option to install Microsoft VsCode (unless you want to give a more elaborate IDE a try!)   

* On Windows the installer will create several new shortcuts in your start menu (under `Anaconda3 (64-bit)`): 

    * Anaconda Navigator - A GUI for managing Anaconda Python (including install and upgrading third-party libraries). It also offers a launcher for key applications such as Jupyter Lab and Spyder).
	* Anaconda Prompt - A command line prompt that allows you to install and upgrade third-party libraries (an alternative to the GUI offered via Anaconda Navigator).
	* JupyterLab - A local version of the notebook server that we're using.
	* Spyder - An integrated desktop environment for Python.

### Code editors
You need a way to write Python code. The best way to do this is to use a dedicated code editor. There are many options out there, so if you already have a preferred one feel free to use it. For new programmers, I suggest the following options (which can be launched from the Anaconda Navigator application):    

* [Spyder IDE](https://www.spyder-ide.org). This is a more traditional development environment that provides you with a Matlab-like file editor, interactive Python prompt and variable browser. This should already have been installed with Anaconda Python. If it's not already installed, you can open up the Anaconda prompt and type `conda install spyder`.

* [JupyterLab](https://jupyter.org). This software allows you to open and  run Jupyter Notebooks on your own computer through the web browser. JupyterLab allows you to open multiple file types side-by-side. If it's not already installed, you can open up the Anaconda prompt and type `conda install jupyterlab`. 

* More advanced IDEs with lots of bells and whistles. These are better for bigger projects and more experienced users. 
  * [Visual Studio](https://visualstudio.microsoft.com/)
  * [PyCharm](https://www.jetbrains.com/pycharm/)

### Course-specific resources
* [NEUS642 on Slack](https://neus642.slack.com) - Our online chatroom. Course staff will try to monitor this when we can. Use this for asking questions.
* [NEUS642 on Github](https://github.com/bburan/NEUS642) - The source code repository for the class. All new files and updates will be posted here.

### Other resources
There are many resources available online for learning Python. [Here are a few](resources.md).
