#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This file contains everything needed to interface with SVN"""

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

# TODO:
# - pysvn for python3 is not available through ubuntu repos
# - possible interesting functions: info2, status, checkout

import subprocess

class IfSVN(object):
    """Main class for the SVN interface"""

    svnclient = None

    def __init__(self):
#        self.svnclient = pysvn.Client()
        pass

    def __del__(self):
        pass

    def checkout_repo(self, cmd_options, course):
        """checkout the repo at url to path"""

        output_path = "./tmp/" + course.name

        # build command
        cmd = ["svn", "checkout", course.svn_path, output_path]

        # TODO:
        # - check if svn really behaves like expected
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()

        # relevant data:
        # print(p.returncode)
        # print(out)

        # TODO:
        # - if hostname can not be resolved (e.g. no network) svn doesn't return an error code -.-

        # returncode is not 0 if e.g. the config xml wasn't found or valid
        if p.returncode != 0:
            return "An pyCheck error occured"






















