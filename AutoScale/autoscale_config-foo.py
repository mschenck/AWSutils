#!/usr/bin/python2.6

from boto.ec2.autoscale import AutoScaleConnection
from ConfigParser import SafeConfigParser
import autoscalelib
import optparse
import boto 
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

    lc = boto.ec2.autoscale.launchconfig.LaunchConfiguration(
        name=config.get("LaunchConfig", 'name'),
        image_id=config.get("LaunchConfig", 'image'),
        key_name=config.get("LaunchConfig", 'key'),
        user_data=config.get("LaunchConfig", 'user_data'),
        security_groups=config.get("LaunchConfig", 'security_groups'),
        instance_type=config.get("LaunchConfig", 'instance_type')
    )
    logging.info( "LC CONFIG = %s" % lc.__dict__ )

    asg = boto.ec2.autoscale.group.AutoScalingGroup(
        group_name=config.get("AutoScaleGroup", 'group_name'),
        availability_zones=config.get("AutoScaleGroup", 'zones'),
        min_size=config.get("AutoScaleGroup", 'min_instances'),
        max_size=config.get("AutoScaleGroup", 'max_instances'),
        launch_config=lc
    )

    print "ASG dict: %s" % asg.__dict__

    asg.connection = aws_connection
    params = {'AutoScalingGroupName' : asg.name }
    asg = aws_connection.get_object(
        'DescribeAutoScalingGroups',
        params,
        boto.ec2.autoscale.group.AutoScalingGroup
    )
    print asg

if __name__ == '__main__':
    main()
    exit
