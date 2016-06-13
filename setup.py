#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from distutils.core import setup
import survey_data_converter.version
import survey_data_converter.info
import py2exe
import os
import sys
from glob import glob
import shutil


def create_build_script():
    dest_dir = os.path.join('build', '_scripts')
    dest_file = os.path.join(dest_dir, 'survey_data_converter')
    src_file = os.path.join('survey_data_converter', '__main__.py')

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    shutil.copyfile(src_file, dest_file)

create_build_script()

sys.path.append("C:\\Windows\\WinSxS\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.1_none_e163563597edeada")
#data_files = [("Microsoft.VC90.CRT", glob(r'C:\Windows\WinSxS\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.1_none_e163563597edeada\*.*'))]

PATH = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(PATH), "survey_data_converter"))

setup(
    version = survey_data_converter.version.__version__,
    description = survey_data_converter.info.__description__,
    name = survey_data_converter.info.__appname__,
    author = survey_data_converter.__author__,
    license = survey_data_converter.__license__,
    #data_files = data_files,
    # targets to build
    windows = [{
        'script': 'build\\_scripts\\survey_data_converter',
    }],
    packages = ['survey_data_converter'],
    )
