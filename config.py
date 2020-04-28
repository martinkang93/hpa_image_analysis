# Configuration settings and aws session manager
#
# This file is intended to be sourced into scripts interfacing with the AWS image server
import boto3
import pymongo

# CONFIG
config = {}

# SECRETS WHICH SHOULD NOT BE TRACKED
# mongo
config['MONGO_USERNAME'] = 'SET IN config.py'
config['MONGO_PASSWORD'] = 'SET IN config.py'

# aws
config['aws_access_key'] = 'SET IN config.py'
config['aws_secret_access_key'] = 'SET IN config.py'


# Constants which are not sensitive and can be tracked
# mongo
config['MONGO_HOST'] = 'mongodb://mongo.servers.nferx.com:27017/'
config['MONGO_PORT'] = 27017
config['MONGO_AUTH_SOURCE'] ='admin'
config['MONGO_AUTH_MECHANISM'] ='SCRAM-SHA-1'

# aws
config['aws_host'] = 'us-east-1'
config['aws_bucket_name'] = 'krzysztof-images'


# Initialize sessions/clients

# mongo
client = pymongo.MongoClient(
    config['MONGO_HOST'], 
    config['MONGO_PORT'],
    username = config['MONGO_USERNAME'], 
    password = config['MONGO_PASSWORD'],
    authMechanism='SCRAM-SHA-1'
)

# aws
session = boto3.Session(
    aws_access_key_id=config['aws_access_key'],
    aws_secret_access_key=config['aws_secret_access_key'],
    region_name=config['aws_host']
)


# Direct execution testing
if __name__ == "__main__":
    print(f"Globals exported by `config.py`")
    print(f"Mongo global client: {client}")
    print(f"AWS global session: {session}")