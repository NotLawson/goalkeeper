# Applets folder
# This folder contains the different applets used by the application.
# This are the user facing components of the application, unlike the modules folder.
# That contains the backend logic of the application.

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
all = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
# __all__ is a list of all the applets in this folder. This is used to import the applets in the main.py file.
# This is used to import the applets in the main.py file.
# We must remove the helper.py file from the list of applets, as it actually isn't.
all.remove('helper')
__all__ = all
