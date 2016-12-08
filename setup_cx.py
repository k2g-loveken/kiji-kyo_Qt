# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

sys.argv.append('build')

build_exe_options = {"packages": ["os"],
                     "excludes": ["tkinter"],
                     "includes": ["PyQt5.QtCore",
                                  "os",
                                  "PyQt5.QtGui",
                                  "PyQt5.QtWidgets",
                                  "PyQt5.QtPrintSupport",
                                  "PyQt5.QtSql",
                                  "jinja2",
                                  "subprocess",
                                  "sqlite3",
                                  "PyQt5.QtWebKitWidgets"],
                     }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "test",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
