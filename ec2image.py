#!/usr/bin/python

from awslib import ec2driver
import urllib

access_key="<AWS access key>"
secret_key="<AWS secret key>"

ec2 = ec2driver(access_key, secret_key)
curl = urllib.FancyURLopener({}) 

uri = ec2.build_uri(
    "GET",
    "DescribeInstanceAttribute",
    [ ("InstanceId", "<instance id>"), ("Attribute", "instanceType") ]
)

print "Performing the following query:"
print uri
print

httpin = curl.open(uri)
print httpin.read()

