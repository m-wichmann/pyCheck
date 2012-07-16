#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Some util functions e.g. to delete checkdout svn repos"""

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

class Util(object):
    """Util class for pyCheck"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    def clean_tmp_dir(self):
        """remove _all_ files in the tmp dir"""
        # get path of this file
        pycheck_dir = os.path.realpath(os.path.dirname(__file__))

        # since this file lies in the src dir, replace src with tmp
        tmp_dir = pycheck_dir[:-3] + "tmp/"

        # walk the tmp dir...
        for root, dirs, files in os.walk(tmp_dir, topdown=False):
            # ...and first remove all files...
            for f in files:
                os.remove(os.path.join(root, f))
            # ...and then all directories.
            for d in dirs:
                os.rmdir(os.path.join(root, d))
