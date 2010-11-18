from boto.ec2.autoscale import LaunchConfiguration,AutoScalingGroup
import logging

################################################################################
# AutoScale: Launch Configuration
################################################################################
def lc_object( lc_name, lc_image, lc_key, lc_user_data, lc_security_groups, lc_instance_type="m1.large" ):
    """ Create a LaunchConfig object for interaction with boto """
    launch_config = LaunchConfiguration(
        name                    = lc_name,
        image_id                = lc_image,
        key_name                = lc_key,
        instance_type           = lc_instance_type,
        user_data               = lc_user_data,
        security_groups         = lc_security_groups
    )
    return launch_config

def lc_exists( conn, lc ):
    """ Check if passed LaunchConfig exists in AWS and returns it if so """
    return conn.get_all_launch_configurations( names=[ lc.name ] )

def create_lc( conn, launch_config ):
    try:
        logging.info( "Creating Launch Configuration [%s]" % launch_config )
        conn.create_launch_configuration( launch_config )
    except Exception, e:
        logging.error( "Caught exception while creating Launch Configuration: %s" % e )

def delete_lc( conn, launch_config ):
    try:
        logging.info( "Deleting Launch Configuration [%s]" % launch_config )
        launch_config.connection = conn
        launch_config.delete()
    except Exception, e:
        logging.error( "Caught exception while deleting Launch Configuration: %s" % e )

################################################################################
# AutoScale:  Auto Scaling Group
################################################################################
def asg_object( as_group_name, as_zones, as_min_instances, as_max_instances, launch_config ):
    as_group = AutoScalingGroup(
        group_name          = as_group_name,
        availability_zones  = as_zones,
        min_size            = as_min_instances,
        max_size            = as_max_instances,
        launch_config       = launch_config
    )
    return as_group

def asg_exists( conn, asg ):
    """ Check to see if an AutoScale Group exists in AWS and returns it if so """
    return conn.get_all_groups( names=[ asg.name ] )

def create_asg( conn, asg ):
    try:
        logging.info( "Creating Auth Scale Group %s" % asg )
        conn.create_auto_scaling_group( asg )
    except Exception, e:
        logging.error( "Caught exception while creating Scaling Group: %s" % e )

def delete_asg( conn, asg ):
    try:
        logging.info( "Deleting AutoScale Group %s" % asg )
        asg.connection = conn
        asg.delete()
    except Exception, e:
        logging.error( "Caught exception while deleting AutoScale Group: %s" % e )

def update_asg( conn, asg ):
    try:
        logging.info( "Updating Group %s" % asg )
        asg.connection = conn
        asg.update()
    except Exception, e:
        logging.error( "Caught exception while updating AutoScale Group: %s" % e )
