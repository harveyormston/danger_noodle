"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['danger_noodle.py']
DATA_FILES = []
OPTIONS = {'iconfile': '/Users/harvey/git/snake_game/danger_noodle.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)