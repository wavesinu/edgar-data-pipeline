import psycopg2
import sys
import boto3
import os

# database connection constants
ENDPOINT = "",
PORT = "5432",
USER = "",
REGION = "",
DBNAME = ""

# get AWS credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER)

try:
    connection = psycopg2.connect(host
except Exception as e:
    print("Database connection failed due to {}".format(e)
