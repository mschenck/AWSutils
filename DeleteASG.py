#!/usr/bin/python

from ec2lib import ec2driver
import urllib

# Account auth details
access_key=""
secret_key=""
allowed_id=""

AutoScalingGroupName=""

ec2 = ec2driver(access_key, secret_key, host="autoscaling.amazonaws.com", version="2009-05-15")

uri = ec2.build_uri(
    "GET",
    "DeleteAutoScalingGroup",
    [
        ("AutoScalingGroupName", AutoScalingGroupName),
    ]
)

print
print uri
print

curl = urllib.FancyURLopener({}) 
httpin = curl.open(uri)
print httpin.read()

