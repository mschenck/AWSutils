import base64
import hmac
import hashlib
import urllib
import time

class ec2driver:
    signature_version="2"
    signature_method="HmacSHA256"
    access_key = ""
    secret_key = ""

    def __init__(self, access_key, secret_key,host="ec2.amazonaws.com", version="2009-11-30"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.ec2_hostname = host
        self.ec2_version = version

    def build_request_dict(self, action, params):
        """ Builds a dictionary of URI components as well as takes a list of tuples for action
            parameters and builds params extenion for request strings
            i.e. [ ( "ImageId.1", "ami-12345678" ) ]  appends "&ImageId.1=ami-12345678" """
        request_attributes = {}
        request_attributes["Action"] = action
        request_attributes["SignatureVersion"] = self.signature_version
        request_attributes["SignatureMethod"] = self.signature_method
        request_attributes["AWSAccessKeyId"] = self.access_key
        request_attributes["Version"] = self.ec2_version

        expire_time = time.strftime( "%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() + 60) )
        timestamp = urllib.quote_plus( expire_time + "Z" )
        request_attributes["Expires"] = timestamp

        for param in params:
            request_attributes[param[0]] = param[1]

        return request_attributes

    def build_request(self, req_dict):
        """ Builds a request string from build_request_dict """
        req_keys = req_dict.keys()
        req_keys.sort()

        first_key = req_keys.pop(0)
        request = first_key + "=" + req_dict[first_key] 
        for key in req_keys:
            request += "&" + key + "=" + req_dict[key]
            
        return request

    def build_string(self, HTTPVerb, request):
        """ Builds a string for signing based on request string from the build_request method """
        string_to_sign = HTTPVerb + '\n' + self.ec2_hostname +'\n' + "/\n" + request
        return string_to_sign

    def sign_string(self, string_to_sign):
        """ Takes a string ready for signing from the build_string method and signs it"""
        hmac_of_string = hmac.new(self.secret_key, string_to_sign, hashlib.sha256).digest()
        signed_string = base64.encodestring(hmac_of_string).strip()
        return signed_string

    def build_uri(self, HTTPVerb, action, params=[]):
        """ returns the final URI for request after building request dictionay, request string and signing """
        req_dict  = self.build_request_dict(action, params)
        request = self.build_request(req_dict)
        req_string = self.build_string(HTTPVerb, request)
        signed_string = self.sign_string(req_string)

        uri = "https://" + self.ec2_hostname + "/?" + request + "&Signature=" + signed_string
        return uri
