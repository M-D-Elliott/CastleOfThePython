import cx_Freeze
import os
import sys

os.environ['TCL_LIBRARY'] = r'C:\Users\Marcus\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Marcus\Python36-32\tcl\tk8.6'

sys.path.append(os.path.abspath('../CastleofthePython7062018p2'))
packages = ["pygame", "Pil", "peewee"]
files = ["world/", "actions/", "weapons/", "monsters/", 'tables.db']
includes = ["scripts/"]
base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cx_Freeze.Executable("game.py", base=base, icon="icon.ico")]

# shortcut table
shortcut_table = [
("DesktopShortcut", # Shortcut
 "DesktopFolder",   # Directory_
 "Castle Of The Python",# Name
 "TARGETDIR",   # Component_
 "[TARGETDIR]\game.exe", # Target
 None,              # Arguments
 None,              # Description
 None,              # Hotkey
 "",                # Icon
 0,                 # IconIndex
 None,              # ShowCmd
 "TARGETDIR",                   # WkDir
 )
]

# table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

cx_Freeze.setup(
    name="Castle of the Python",
    options={"bdist_msi": bdist_msi_options,
             "build_exe": {"packages": packages, "include_files": files, "includes": includes}},
    executables=executables,
    version="0.3"
)


# python setup.py bdist_msi
