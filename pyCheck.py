#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main file for pyCheck"""

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
# - add logger. I guess it's enough if the logger is available in this class?!
# - split main function into some subfunctions

from optparse import OptionParser
from optparse import OptionGroup
import os
import subprocess
import logging.handlers


# All imports to test if it works
import src.config as config
import src.ifCS as ifCS
import src.ifJUnit as ifJUnit
import src.ifSVN as ifSVN
import src.jcompile as jcompile
import src.model as model
import src.output as output
import src.util as util
import src.xmlop as xmlop


PYCHECK_VERSION = "0.1"

class pyCheck(object):
    """Main class for pyCheck"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    def pycheck_main(self):
        """pyCheck main function"""

        # init logger
        logger = self.__init_logger()

        # init for later use
        util_obj = util.Util()
        junit = ifJUnit.IfJUnit()
        checkstyle = ifCS.IfCS()
        svn = ifSVN.IfSVN()
        output_obj = output.Output()
        jcompile_obj = jcompile.JCompile()

        ##########
        # parse cmd line options
        cmd_options = self.__parse_options()

        # TODO: output cmd options seperatly to logfile
        logger.info("PyCheck started with following command line options:")
        logger.info(cmd_options)

        ##########
        # check cmd options for options that would quit programm early...
        if cmd_options.validate_config is True:
            self.__validate_config()

            # return/quit early
            return

        if cmd_options.test_pycheck is True:
            self.__test_pycheck()

            # return/quit early
            return

        ##########
        # parse xml file options
        # returns some option objects
        logger.info("Parsing XML options")
        xmlop_obj = xmlop.XMLOptionParser()

        checkstyle_config = xmlop_obj.parse_checkstyle_cfg("./cfg/checkstyle.xml")
        junit_config = xmlop_obj.parse_junit_cfg("./cfg/junit.xml")
        jcompile_config = xmlop_obj.parse_jcompile_cfg("./cfg/jcompile.xml")
        courses_config = xmlop_obj.parse_courses_cfg("./cfg/courses/")

        ##########
        # do something with the options from cmd line and xml files
        # TODO: mhh... I'm not sure anymore that this makes sense?!
        configs = self.__merge_configs(cmd_options, checkstyle_config, junit_config, jcompile_config, courses_config)

        ##########
        # iterate over courses
        for course in configs["courses_config"]:
            logger.info("Current course: " + course.name)

            ##########
            # svn checkout and check if current version was already checked (auxilary data)
            # - checkout course main svn to ./tmp/ from course.svn_path
            if cmd_options.skip_svn is not True:
                logger.info("SVN checkout...")
                svn.checkout_repo(cmd_options, course)

            ##########
            # iterate over groups in ./tmp/
            temp = os.listdir('./tmp/'+ course.name)
            groupdirs = []
            for directory in temp:
                if os.path.isdir('./tmp/' + course.name + '/' + directory):
                    groupdirs.append(directory)

            logger.info("Exercise count: " + str(len(course.exercises)))
            logger.info("Group count: " + str(len(groupdirs)))

            ##########
            # iterate over groups in ./tmp/GROUP/
            for groupdir in groupdirs:

                # TODO: maybe make this into a dict
                junit_results = []
                checkstyle_results = []

                ##########
                # iterate over exercises
                for exercise in course.exercises:

                    # build path for this exercise
                    current_dir = './tmp/' + course.name + '/' + groupdir + '/' + exercise.name

                    ##########
                    # compile java code
                    if cmd_options.skip_compile is not True:
                        # TODO
                        print("Compiling java code...")
                        jcompile_obj.compile_project(current_dir, jcompile_config, course)

                    ##########
                    # junit tests
                    # return result object
                    junit_result = None
                    if cmd_options.skip_junit is not True:
                        # TODO
                        print("JUnit test...")
                        temp = junit.run_junit_test(current_dir, junit_config, exercise)
                        junit_results.append(temp)

                    ##########
                    # checkstyle
                    # return result object
                    checkstyle_result = None
                    if cmd_options.skip_checkstyle is not True:
                        # TODO
                        print("Running Checkstyle...")
                        temp = checkstyle.run_checkstyle(current_dir, checkstyle_config, exercise)
                        checkstyle_results.append(temp)

                ##########
                # output results for all exercises to file
                if cmd_options.skip_output is not True:
                    # TODO
                    print("Generating results...")
                    output_obj.generate_result(junit_results, checkstyle_results, course)

            ##########
            # clean up the checkedout repo
#            print("Cleaning SVN Repos...")
#            util_obj.clean_tmp_dir()



    def __parse_options(self):
        """parse cmd line options"""

        # get OptionParser object; set --version output
        parser = OptionParser(version="%prog " + str(PYCHECK_VERSION))

        # add basic options
        parser.add_option("-c", "--clean", action="store_true", dest="clean", help="clean pyCheck dir. This deletes compiled python files as well as auxilary data and output data.")
        parser.add_option("-q", "--quiet", action="store_true", dest="quiet", help="silence output of pyCheck")
        parser.add_option("--validate-config", action="store_true", dest="validate_config", help="validate config against xsd files")
        
        # add debug options to seperate group
        debug_group = OptionGroup(parser, "Debug Options", "These should only be necassary to find bugs.")

        debug_group.add_option("--skip-svn", action="store_true", dest="skip_svn", help="skip svn phase (checkout and revision check)")
        debug_group.add_option("--skip-compile", action="store_true", dest="skip_compile", help="skip compile phase")
        debug_group.add_option("--skip-junit", action="store_true", dest="skip_junit", help="skip junit phase")
        debug_group.add_option("--skip-checkstyle", action="store_true", dest="skip_checkstyle", help="skip checkstyle phase")
        debug_group.add_option("--skip-output", action="store_true", dest="skip_output", help="skip output phase")
        debug_group.add_option("--test-pycheck", action="store_true", dest="test_pycheck", help="do some debug tests for pycheck. e.g. xsd validation")

        parser.add_option_group(debug_group)

        # parse options
        (options, args) = parser.parse_args()
        
        # return only the interesting part
        return options


    def __merge_configs(self, cmd_options, checkstyle_config, junit_config, jcompile_config, courses_config):
        """merge all configs to one object, that can be passed on to other functions"""

        # init empty dict
        ret = {}

        # TODO:
        # - at this point the options may be altered

        # add option elements to dict
        ret["cmd_options"] = cmd_options
        ret["checkstyle_config"] = checkstyle_config
        ret["junit_config"] = junit_config
        ret["jcompile_config"] = jcompile_config
        ret["courses_config"] = courses_config

        # return options
        return ret


    def __init_logger(self):
        """Init and return logger."""
        # get logger object
        logger = logging.getLogger('pyCheck')
        logger.setLevel(logging.DEBUG)

        # set file handle for log file
        # use a rotating log file with max 200kb and backup up to 3 log files
        logfile = './log/pyCheck.log'
        try:
            log_fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=200000, backupCount=3)
        except IOError:
            print("Could not open log file!")
            return None

        log_fh.setLevel(logging.DEBUG)
        # set formatter for logger
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)-8s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        log_fh.setFormatter(formatter)
        # add file handle to logger
        logger.addHandler(log_fh)

        logger.info("==========")

        return logger




    def __validate_config(self):
        """validate config files against xsd files"""

        # determine pycheck src dir
        pycheck_dir = os.path.realpath(os.path.dirname(__file__))

        # print info
        print("Validating config files against xsd definition...")
        print("This will need xmllint installed!\n")

        # init check value
        ret = 0

        # validate junit.xml
        ret += self.__call_xmllint(pycheck_dir + "/xsd/junit.xsd", [pycheck_dir + "/cfg/junit.xml"])
        # validate checkstyle.xml
        ret += self.__call_xmllint(pycheck_dir + "/xsd/checkstyle.xsd", [pycheck_dir + "/cfg/checkstyle.xml"])

        # validate course configs
        dirlist = os.listdir(pycheck_dir + os.sep + "cfg" + os.sep + "courses")

        courselist = []

        # iterate over cfg files
        for d in dirlist:
            # build path to file
            filepath = pycheck_dir + os.sep + "cfg" + os.sep + "courses" + os.sep + d + os.sep + "course_config.xml"
            courselist.append(filepath)

        ret += self.__call_xmllint(pycheck_dir + "/xsd/course.xsd", courselist)

        # if one of these files did not validate, ret is not 0
        if ret == 0:
            print("\nAll config files validate!")
        else:
            print("\nSome error occured! Maybe there is an error in one of the config files!")


    def __test_pycheck(self):
        """test pyCheck files. e.g. xsd validation against W3C XML Schema"""

        # determine pycheck src dir
        pycheck_dir = os.path.realpath(os.path.dirname(__file__))

        # print info
        print("Validating xsd files against XML Schema definition...")
        print("This will need xmllint installed and an internet connection for the W3C XML Schema!\n")

        # get xsd files and add the path
        xsd_files = os.listdir(pycheck_dir + "/xsd/")
        xsd_files_path = []
        for f in xsd_files:
            xsd_files_path.append(pycheck_dir + "/xsd/" + f)

        # call xmllint
        ret = self.__call_xmllint("http://www.w3.org/2001/XMLSchema.xsd", xsd_files_path)

        if ret == 0:
            print("\nAll xsd files validate!")
        else:
            print("\nSome error occured! Maybe there is an error in one of the xsd files!")
        

    def __call_xmllint(self, schema, files):
        """call xmllint. files has to be a list"""

        # test if argument files is a list
        # this is necesarry since a string can be iterated like a list
        if isinstance(files, list) == False:
            raise TypeError("Argument files has to be a list of strings!")

        # build basic cmd
        cmd = ["xmllint", "--noout", "-schema"]

        # append the schema
        cmd.append(schema)

        # append files to validate
        for f in files:
            cmd.append(f)

        ret = 0

        # call xmllint and store return value
        try:
            ret = subprocess.call(cmd)
        except OSError:
            print("OS error occured! Maybe xmllint is not installed?!")

        # everything but 0 is unacceptable
        if ret == 0:
            return 0
        else:
            return 1


if __name__ == '__main__':
    mainobj = pyCheck()
    mainobj.pycheck_main()
