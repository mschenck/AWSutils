#!/usr/bin/python2.6

from boto.ec2.autoscale import AutoScaleConnection
from ConfigParser import SafeConfigParser
import autoscalelib
import optparse
import sys
import os

import logging
logging.basicConfig(level=logging.INFO)

class SuperConfigParser( SafeConfigParser ):
    def get(self, section, option):
        """ Get a parameter if the returning value is a list, convert string value to a python list"""
        value = SafeConfigParser.get(self, section, option)
        if len(value) > 0:
            if (value[0] == "[") and (value[-1] == "]"):
                return eval(value)
            else:
                return value
        return value

def parse_config( file ):
    config = SuperConfigParser()
    try:
        config.read( os.path.expanduser( file ) )
    except Exception, e:
        logging.error( "Caught following exception while attempting to read config file %s: %s" % ( file, e ) )
        sys.exit(1)
    return config


def main():
    parser = optparse.OptionParser()
    parser.add_option( "-c", "--config", dest="config_file", help="AutoScale config INI", metavar="FILE" )
    (options, args) = parser.parse_args()
    logging.info( "Using config file [%s]" % options.config_file )

    config = parse_config( options.config_file ) 

    aws_access = config.get("AWS", 'access')
    aws_secret = config.get("AWS", 'secret')

    logging.debug( "Connecting to AWS with access [%s] and secret [%s]" % ( aws_access, aws_secret ) )
    aws_connection = AutoScaleConnection( aws_access, aws_secret )

    print "AutoScalingGroups:"
    lcs = aws_connection.get_all_launch_configurations()
    for lc in lcs:
        print "%s -> %s" % (lc, lc.__dict__ )

if __name__ == '__main__':
    main()
    exit
