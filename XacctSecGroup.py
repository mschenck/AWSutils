#!/usr/bin/python

from ec2lib import ec2driver
import urllib

# Account that you are creating the rule on
access_key=""
secret_key=""

# Account to allow access
allowed_id="017019116779" 

# Service details to which access is being granted
protocol="tcp"
src_port="9090"
dst_port="9090"
src_group="default"
dst_group="default"

ec2 = ec2driver(access_key, secret_key)

uri = ec2.build_uri(
    "GET",
    "AuthorizeSecurityGroupIngress",
    [
        ("GroupName", dst_group),
        ("IpPermissions.1.IpProtocol", protocol),
        ("IpPermissions.1.FromPort", src_port),
        ("IpPermissions.1.ToPort", dst_port),
        ("IpPermissions.1.Groups.1.GroupName", src_group),
        ("IpPermissions.1.Groups.1.UserId", allowed_id),
    ]
)

print
print uri
print

curl = urllib.FancyURLopener({}) 
httpin = curl.open(uri)
print httpin.read()

