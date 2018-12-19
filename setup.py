import cx_Freeze
import os
import sys

os.environ['TCL_LIBRARY'] = r'C:\Users\Marcus\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Marcus\Python36-32\tcl\tk8.6'

sys.path.append(os.path.abspath('../CastleofthePython7062018p2'))
packages = ["pygame", "Pil", "peewee", "sys", "time", "os", "math"]
files = ["world/", "actions/", "level/", "weapons/", "monsters/"]
includes = ["scripts/"]
base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cx_Freeze.Executable("game.py", base=base)]
cx_Freeze.setup(
    name="Castle of the Python",
    options={"build_exe": {"packages": packages, "include_files": files, "includes": includes}},
    executables=executables,
    version="0.3"
)
# python setup.py bdist_msi
