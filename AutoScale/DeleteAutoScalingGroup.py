#!/usr/bin/python2.6

from boto.ec2.autoscale import AutoScaleConnection
from ConfigParser import SafeConfigParser
import autoscalelib
import optparse
import time
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
    parser.add_option( "-a", "--asg", dest="asg_name", help="AutoScaleGroup Name to be deleted", metavar="ASG" )
    (options, args) = parser.parse_args()
    logging.info( "Using config file [%s]" % options.config_file )

    config = parse_config( options.config_file ) 

    aws_access = config.get("AWS", 'access')
    aws_secret = config.get("AWS", 'secret')

    lc = autoscalelib.lc_object(
        config.get("LaunchConfig", 'name'),
        config.get("LaunchConfig", 'image'),
        config.get("LaunchConfig", 'key'),
        config.get("LaunchConfig", 'user_data'),
        config.get("LaunchConfig", 'security_groups'),
        config.get("LaunchConfig", 'instance_type')
    )
    logging.debug( "LC CONFIG = %s" % lc.__dict__ )

    asg = autoscalelib.asg_object(
        config.get("AutoScaleGroup", 'group_name'),
        config.get("AutoScaleGroup", 'zones'),
        config.get("AutoScaleGroup", 'min_instances'),
        config.get("AutoScaleGroup", 'max_instances'),
        lc
    )

    aws_connection = AutoScaleConnection( aws_access, aws_secret )
    asg.connection = aws_connection
    asg.shutdown_instances()
    while asg.instances:
        logging.info( "Waiting to remove ASG %s, remaining instance(s) %s" % (asg, asg.instances ) )
        time.sleep(5)
    asg.delete()

if __name__ == '__main__':
    main()
    exit
