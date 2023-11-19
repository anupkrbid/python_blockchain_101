# Python Blockchain 101

Building a simple blockchain and cryptocurrency app while learning python 3.x

Learn more about the History of Python: https://en.wikipedia.org/wiki/History_of_Python

Python 2.7 vs 3.x: https://wiki.python.org/moin/Python2orPython3

Python vs other Programming Languages: https://www.cleveroad.com/blog/python-vs-other-programming-languages

More on Python Basics: https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator

More on Python Functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

Python Floating Point Precision: https://docs.python.org/3/tutorial/floatingpoint.html

PEBs: https://www.python.org/dev/peps/

PEB 8 - Style Guide: https://www.python.org/dev/peps/pep-0008/

String Escape Characters: http://python-reference.readthedocs.io/en/latest/docs/str/escapes.html

Example Docstrings: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

More on the Python Extension for Visual Studio Code: https://code.visualstudio.com/docs/languages/python

More on Loops: https://docs.python.org/3/tutorial/controlflow.html#for-statements

More on if Statements: https://docs.python.org/3/tutorial/controlflow.html#if-statements

More on Data Structures: https://docs.python.org/3/tutorial/datastructures.html

More on format() : https://docs.python.org/3.4/library/functions.html#format

More on the Python format() Mini-Language: https://docs.python.org/3.4/library/string.html#formatspec

Python Lambda Functions: https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions

map() : https://docs.python.org/3/library/functions.html#map

reduce() : https://docs.python.org/3/library/functools.html#functools.reduce

The (Standard) Library Reference: https://docs.python.org/3/library/index.html

Reading and Writing Files: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

More on the json Package: https://docs.python.org/3/library/json.html

More on the pickle Package: https://docs.python.org/3/library/pickle.html

Debugging Python in Visual Studio Code: https://code.visualstudio.com/docs/python/debugging

More on try-except: https://docs.python.org/3/tutorial/errors.html

Docstring Examples: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Python Special Methods: https://docs.python.org/3/reference/datamodel.html#basic-customization

Using Virtual Environments
Virtual Environments allow you to only install certain Python packages for some projects - instead of globally on your machine. This is helpful when working with multiple projects where you might want to use a different set of packages (=> dependencies) for every project.

You can easily create a new virtual environment in the Anaconda Navigator (as shown in the last lecture). Read more here: https://docs.anaconda.com/anaconda/navigator/getting-started#navigator-managing-environments

After creating an environment, you need to activate it. There are two ways of doing that:

Execute source activate NAME_OF_ENVIRONMENT (e.g. source activate pycoin ) on macOS and Linux or just activate NAME_OF_ENVIRONMENT (e.g. activate pycoin ) on Windows. This might fail for Windows though. To fix it, please see this thread: https://github.com/ContinuumIO/anaconda-issues/issues/2533
Alternatively, you use the Anaconda Navigator to launch a terminal/ command prompt that already uses your new virtual environment: Click on the green "play" button next to your environment name and choose the option to launch a new terminal/ command prompt there. This will be a normal terminal/ command prompt, so after navigating into your project folder (via the cd command), you can use it just as shown in the videos.
