# YAML Parser

A simple [YAML](http://www.yaml.org/) file parser with production not dev in mind.

## What doest it do?

The most common mistake about YAML files is the TAB char instead of a space char.  The script allow to replace the tab char.

Then the file is parsed with PyYAML and indicate where is the problem.

## How to install it?

You can either install the script as a program with `setup.py` or directly by the and with the shell script

## The `setup.py` way:

Just type in the project directory:

    $ sudo python setup.py install

or if you want to install it in a specific directory:

    $ python setup.py install 

## How to use it?

To use `yaml
    yaml_parser.py the_yaml_file.yml
    
 