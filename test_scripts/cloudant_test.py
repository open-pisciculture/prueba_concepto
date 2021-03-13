#!/usr/bin/python3

USERNAME = 'apikey-v2-26nq5kwzc5hwx3stwpswvpgbkrfvfpxkpcig58782ss3'
PASSWORD = '7c0ec7e967d8ef10ceb70c1ee164c139'
ACCOUNT_NAME = 'alejandroariaszuluaga@gmail.com'
API_KEY = 'DttkhHtdEaQ_ywM857D3qrbT-_LIrxAC8t2wd7Wrz8YM'
URL = 'https://apikey-v2-26nq5kwzc5hwx3stwpswvpgbkrfvfpxkpcig58782ss3:7c0ec7e967d8ef10ceb70c1ee164c139@69d17e12-ebf6-496d-8bfc-2d5deb4c7b00-bluemix.cloudantnosqldb.appdomain.cloud'

# Use CouchDB to create a CouchDB client
# from cloudant.client import CouchDB
# client = CouchDB(USERNAME, PASSWORD, url='http://127.0.0.1:5984', connect=True)

# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant

# Authenticate using an IAM API key
# client = Cloudant.iam(None, API_KEY, url=URL, connect=True)

# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
# or using url
client = Cloudant(USERNAME, PASSWORD, url='https://acct.cloudant.com')

# or with a 429 replay adapter that includes configured retries and initial backoff
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   adapter=Replay429Adapter(retries=10, initialBackoff=0.01))

# or with a connect and read timeout of 5 minutes
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   timeout=300)

print(client)
# Perform client tasks...
# session = client.session()
# print(session)
# print('Username: {0}'.format(session['userCtx']['name']))
# print('Databases: {0}'.format(client.all_dbs()))

my_database = client.create_database('my_database')

# You can check that the database exists
if my_database.exists():
    print('SUCCESS!!')


# Disconnect from the server
client.disconnect()