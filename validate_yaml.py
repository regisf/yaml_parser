#!/usr/bin/env python
#
# Copyright © 2016  Regis FLORET 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files 
# (the “Software”), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
#

"""
Validate yaml is a simple YAML validator for the sys admin of my
compagny.

Please Fabien, stop crying on me about those files, I'm not 
responsible ^^
"""

import sys
import argparse
from cStringIO import StringIO
import yaml


class Options:
    """ Global options """
    stop_on_error = False
    indent = 0
    replace_tab = False
    verbose = False
    files = []
    
    def __repr__(self):
        """Class representation. Debug purpose only """
        return """<Options stop_on_error: {}, indent={}, replace_tab={}, verbose={}, files={}>""".format(
            self.stop_on_error, 
            self.indent, 
            self.replace_tab,
            self.verbose, 
            self.files
        )  
            
    def parse(self, result):
        """
        Convert result from command line to direct access variables 

        :param result: The result from ArgumentParser
        :type result: argparse.Namespace
        """

        self.replace_tab = result.replace_tab
        self.stop_on_error = result.stop_on_error
        self.files = result.files
        self.indent = result.indent
        self.verbose = result.verbose

options = Options()



class Color:
    """ Convinient class to display colors """
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
   
    @staticmethod
    def prepare(color, msg):
        return Color.BOLD + color + msg + Color.END
        
    @staticmethod
    def critical(msg, use_stderr=False):
        """ 
        Display a critical message in RED BOLD
        
        :param msg: The message to display
        :type msg: str
        """
        msg = Color.prepare(Color.RED, " Error: " + msg)
        
        if not use_stderr:
            sys.exit(msg)
        else:
            sys.stderr.write(msg)
      
    @staticmethod
    def warning(msg):
        """ 
        Display a warning message in YELLOW BOLD
        
        :param msg: The message to display
        :type msg: str
        """
        print Color.prepare(Color.YELLOW, " Warning " + msg)
      
         
    @staticmethod
    def success(msg):
        """ 
        Display a warning message in YELLOW BOLD
        
        :param msg: The message to display
        :type msg: str
        """
        print Color.prepare(Color.GREEN, " Success: " + msg)
        

def process_yaml_file(filename):
    """
    Open a file and replace tab with spaces if --replace-tab option and --indent are set
    Also, parse the YAML file. if an error occured, exit
    and remove \r and trailing space char if exists and if the --clean argument 
   
    :param filename: The complete path
    :type filename: str
	"""
    out_stream = StringIO()
    
    with open(filename, "r") as file_to_validate:
        line_count = 0
        in_stream = StringIO(file_to_validate.read())
        
        for l in in_stream:
            line_count += 1;
            if '\t' in l:
                Color.critical("Not well formed YAML file. TAB char at line {}".format(line_count), True)

                if options.stop_on_error:
                    print
                    sys.exit(1)
                                    
                if options.replace_tab:
                    Color.success("Replaced")
                    print
                    l = l.replace("\t", " " * options.indent)
            out_stream.write(l)
            
        in_stream.close()

        
        try:
            yaml_parser = yaml.load(out_stream.getvalue())
            yaml.dump(yaml_parser)            
            
        except yaml.scanner.ScannerError as e:
            print Color.BOLD + Color.RED + str(e) + Color.END
            
            if options.stop_on_error:
                sys.exit(1)

    if options.replace_tab:
        with open(filename, "w") as file_to_write:
            file_to_write.write(out_stream.getvalue())
            out_stream.close()
    

def process_args():
    """ Process the argument line and set the options
    """
    parser = argparse.ArgumentParser(
        description="Parse to ensure the validity of a YAML file",
        epilog="And you never should trust developers when they say: It's a better way to do it"
    )
    parser.add_argument(
        "--replace-tab", 
        action="store_true", 
        help="Replace tab characters when found"
    )
    parser.add_argument(
        "--indent",
        metavar='N',
        type=int,
        help="Set the indent space when --replace-tab is set"
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true", 
        help="Stop on first error found"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files lists"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Display information on what the program is doing"
    )
    
    options.parse(parser.parse_args())
   
    
    if options.replace_tab and not options.indent:
        Color.critical("--replace-tab require --indent argument")
        
    if not options.replace_tab and options.indent:
        Color.warning("This is not useful too add --indent argument without --replace-tab")
    
    if options.stop_on_error and options.replace_tab:
        Color.warning("Tab replacement is not effective with --replace-tab option")


if __name__ == '__main__':
    process_args()
        
    if options.files:
        for file_from_cmd in options.files:
            process_yaml_file(file_from_cmd)
    else:
        Color.critical("Need YAML file to process.")

