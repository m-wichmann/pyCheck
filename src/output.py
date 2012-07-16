#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Everything in this file generates or deals with output"""

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

class Output(object):
    """Main class for output"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    def generate_result(self, junit_results, checkstyle_results, course, output_path=None):
        """output all results to a conviniet form"""
        # take junit_result and checkstyle_results and generate output (to output_path) for group
        pass
