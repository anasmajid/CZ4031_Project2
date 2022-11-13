# CZ4031 Project 2: Connecting Queries with Query Plans

## Installation of Libraries

1. The required python libraries are included in the requirements.txt file, and can be installed using the following command:  \
> *python -m pip install -r requirements.txt*

2. The GraphViz executables need to be installed separately. Download and run the installer that is found here:  \
*<center> https://graphviz.org/download/ </center>*

3. Set the GraphViz/bin folder in the Windows environment PATH variable, and restart all open terminals. Please see the **Additional Notes** section if any issues are encountered.

## Running the application

1. The entry point for the application is in *project.py*. Run the application using the following command with the dependencies installed:
> *python project.py*

## Overview of files

- interface.py contains the code for the GUI.
- annotation.py contains code for generating the annotations
- preprocessing.py file contains code for reading inputs and other necessry preprocessing.
- project.py is the main file that invokes the application.

## Additional Notes

1. The GraphViz library is used to generate a visual flowchart representation of the QEP and the AQP. Functions from this library are called when the "Show Query Tree" button is pressed. The library is not required for any other functionality of our application.

2. In case of an instance of "OSError" that are in relation to GraphViz/dot, please check that the python library as well as the GraphViz executables (using the installer) have been installed correctly.

3. The GraphViz/bin folder in the Windows environment PATH variable, and the terminal used to run our application needs to be restarted after changing the PATH variable.

4. If GraphViz errors persist, please restart the system after updating the path and try again.

5. Sample images of the QEP and AQP flowcharts generated using this functionality are also included in our report.