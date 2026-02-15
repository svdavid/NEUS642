## NEUS 642 Week 7: miniML (AI-based framework for the detection of synaptic events)

To use miniML, we first need to set up a virtual environment from your command line (e.g., anaconda prompt or terminal). We will use an older version of python that is compatible with miniML. 

`conda create -n miniML python=3.10.11`

`conda activate miniML`

Next, we will install git and clone the respository. We want the files from github to be in a folder called "miniML" that is in the same folder as "NEUS642". When you run `git clone` make sure your command line looks like: C:\Users\...\[Whichever folder that "NEUS642" is in]

`conda install git`

`git clone https://github.com/delvendahl/miniML.git`

`cd miniML`

Now your command line should look like C:\Users\...\[Whichever folder that "NEUS642" is in]\miniML.

Next we need to install the required packages to run miniML:

`pip install jupyterlab`

`pip install -r requirements.txt`

The version of matplotlib in requirements.txt is too old. Also, we will use PyQt to make our plots more interactive.

`pip install matplotlib==3.7.0 'PyQt5>=5.15.10'`

Be aware of potential issues when installing with both conda and pip. Try to stick to just one method as much as you can (pip worked best for me), as mixing the two can cause dependency conflicts. 

A GPU is not required for model inference or model training, but if you do want to use one, install tensorflow metal/CUDA (look up compatibility based on OS and GPU hardware). Kaggle is available for cloud computing if a GPU is not available. 

If you'd like to use the GUI in the future, additional packages (requirements_gui.txt) are required. Remember to update matplotlib.

Now we move our current directory back so we can access this week's exercise.

`cd ..\`

Now that we are finished setting up, open jupyter lab and navigate to this week's exercise.

`jupyter lab`