# -*- coding: utf-8 -*-
from distutils.core import setup
import sys
import py2exe

sys.argv.append('py2exe')

option = {
    'bundle_files': 1,
    'compressed': True,
    'includes': [
                "PyQt5.QtWidgets",
                "PyQt5.QtPrintSupport",
                "PyQt5.QtNetwork",
                "PyQt5.QtCore",
                "PyQt5.QtWebKitWidgets",
                "ui",
                "sub",
                "PyQt5.QtWebKit",
                "subprocess",
                # "ui.Ui_Form",
                # "sub.Ui_Dialog"
                "sip",
                ],
    'packages': [
                # "sys",
                # "os",
                "jinja2",
                "sqlite3",
                ]

}
setup(
    options={'py2exe': option},
    windows=[{
            'script': 'main.py',
            'icon_resources': [(1, 'icon.ico')],
            }],
    zipfile=None, requires=['jinja2']
)
