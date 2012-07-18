#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This file contains util functions to compile java projects"""

#####
# pyCheck
#
# Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this software; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

import os
import subprocess

class JCompile(object):
    """Compile java/eclipse project"""

    __JAVA_SRC_SUFFIX = '.java'

    def __init__(self):
        pass


    def __del__(self):
        pass


    def compile_project(self, project_path, jcompile_config, course):
        """compile every .java file located in the given path"""

        print(jcompile_config)

        # TODO:
        # - get config data and use it
        # - define the Classpath
        # - call the actual compiler!

        # all .java src files located in the project_path folder
        src_files = self.__filter_src_files(project_path)

        if len(src_files) == 0:
            return

        # build command
        # TODO:
        # java -cp /path/to/classpath:/more/classpath
        cmd = ["javac"]

        for f in src_files:
            cmd.append(f)

        print("jcompile")
        print(cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()

        # returncode is not 0 if somethin went wrong
        if p.returncode != 0:
            return "An pyCheck error occured"




    def __filter_src_files(self, project_path):
        """recursivly iterate through project tree searching for .java src files"""
        
        # return list
        src_files = []

        # recursivly walk all directories
        for root, dirs, files in os.walk(project_path):
            # iterate over files in current dir
            for f in files:
                # only select file if it ends in .java
                if (f.find(self.__JAVA_SRC_SUFFIX) == len(f) - len(self.__JAVA_SRC_SUFFIX)):
                    # save path for later use
                    src_files.append(os.path.join(root, f))

        # return list of all .java src files
        return src_files
