#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All xml stuff is handled in this file"""

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

import xml.dom.minidom as dom
import os

import src.model as model

# TODO:
# - maybe check if config has changed via hash?!
# - handle some exeptions (file not found...)

class XMLOptionParser(object):
    """This class handles all XML operations"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    def parse_checkstyle_cfg(self, filepath):
        """filepath is the path to the checkstyle.xml"""

        # parse file to tree
        tree = dom.parse(filepath)

        # init empty dict for return infos
        ret = {}

        # iterate through all childs of "head" node (config)
        for element in tree.firstChild.childNodes:
            # if node is of "type"
            if element.nodeName == "bin-path": 
                # access Text object and "info"
                ret["bin-path"] = element.firstChild.data
            if element.nodeName == "checkstyle-config": 
                # access Text object and "info"
                ret["checkstyle-config"] = element.firstChild.data

        # return parsed data
        return ret


    def parse_junit_cfg(self, filepath):
        """filepath is the path to the junit.xml"""

        # parse file to tree
        tree = dom.parse(filepath)

        # init empty dict for return infos
        ret = {}

        # iterate through all childs of "head" node (config)
        for element in tree.firstChild.childNodes:
            # if node is of "type"
            if element.nodeName == "bin-path": 
                # access Text object and "info"
                ret["bin-path"] = element.firstChild.data

        # return parsed data
        return ret


    def parse_jcompile_cfg(self, filepath):
        """filepath is the path to the jcompile.xml"""

        # parse file to tree
        tree = dom.parse(filepath)

        # init empty dict for return infos
        ret = {}

        # iterate through all childs of "head" node (config)
        for element in tree.firstChild.childNodes:
            # if node is of "type"
            if element.nodeName == "bin-path": 
                # access Text object and "info"
                ret["bin-path"] = element.firstChild.data
            if element.nodeName == "args": 
                # access Text object and "info"
                ret["args"] = element.firstChild.data

        # return parsed data
        return ret


    def parse_courses_cfg(self, dirpath):
        """dirpath has to be the path in wich all course configs are.
        This function return a list of all courses.
        The items in this list are dicts that contain data for one course
        """

        # TODO: all this os stuff depends on... well... the os. We should be extra careful!

        # normalize the path so we don't get any problems
        dirpath = os.path.abspath(dirpath)
        dirpath = os.path.normpath(dirpath)

        # empty list for return data
        ret = []

        # get list of all course configs
        # TODO: only select real course cfg
        dirlist = os.listdir(dirpath)

        # iterate over cfg files
        for d in dirlist:
            if d == '.svn':
                continue
            # build path to file
            filepath = dirpath + os.sep + d + os.sep + "course_config.xml"
            # parse cfg file
            tree = dom.parse(filepath)
            # let another function handle the tree and append retrieved data
            ret.append(self.__parse_course_tree(tree))

        # return parsed data
        return ret


    def __parse_course_tree(self, tree):
        """parse the subtree for a course"""

        # init empty Course object
        ret = model.Course()

        # iterate through all childs of "head" node (course)
        for element in tree.firstChild.childNodes:
            # course name
            if element.nodeName == "name":
                ret.name = element.firstChild.data
            # svn path
            if element.nodeName == "svn-path":
                ret.svn_path = element.firstChild.data
            # course advisers
            if element.nodeName == "advisers":
                ret.advisers = self.__parse_advisers_tree(element)
            # course exercises
            if element.nodeName == "exercises":
                ret.exercises = self.__parse_exercises_tree(element)

        # return Course
        return ret


    def __parse_advisers_tree(self, tree):
        """parse the advisers subtree"""
        ret = []

        # iterate over advisers and store in list
        for adviser in tree.childNodes:
            
            if adviser.nodeName == "adviser":
                obj = model.Adviser()
                obj.name = adviser.firstChild.data

                ret.append(obj)

        return ret


    def __parse_exercises_tree(self, tree):
        """parse exercises subtree"""
        ret = []

        # iterate over advisers and store in list
        for exercise in tree.childNodes:
            if exercise.nodeName == "exercise":

                obj = model.Exercise()

                for element in exercise.childNodes:

                    name = ""
                    checkstyle_config = ""
                    test_class_path = ""
                    omit_junit = False

                    if element.nodeName == "name":
                        obj.name = element.firstChild.data
                    if element.nodeName == "checkstyle-config":
                        obj.checkstyle_config = element.firstChild.data
                    if element.nodeName == "test-class-path":
                        obj.test_class_path = element.firstChild.data
                    if element.nodeName == "omit-junit":
                        obj.omit_junit = element.firstChild.data
                        
                ret.append(obj)

        return ret











