#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This file contains everything needed to interface with Checkstyle"""

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
# - checkstyle -c sun_checks.xml -r java/

import os
import subprocess

class IfCS(object):
    """Main class for the Checkstyle interface"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    def run_checkstyle(self, project_dir, checkstyle_config, exercise):
        # define checkstyle xml config global or locally
        cs_config_xml = checkstyle_config["checkstyle-config"]
        if exercise.checkstyle_config != "":
            cs_config_xml = exercise.checkstyle_config

        # build command
        cmd = [checkstyle_config["bin-path"], "-c", cs_config_xml, "-f", "xml", "-r", project_dir]

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()

        # relevant data:
#        print(p.returncode)
#        print(out)

        # returncode is not 0 if e.g. the config xml wasn't found or valid
        if p.returncode != 0:
            return "An pyCheck error occured"

#        xml_output = str(out).replace("\\n","")
#        print(xml_output)

#        import xml.dom.minidom as dom

#        dom_out = dom.parseString(xml_output)
#        print(dom_out)














