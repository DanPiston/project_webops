from requests_oauthlib import OAuth1Session
import time
from pprint import pprint
import config

aweber = OAuth1Session(client_key=config.CLIENT_KEY,
                       client_secret=config.CLIENT_SECRET,
                       resource_owner_key=config.RESOURCE_OWNER_KEY,
                       resource_owner_secret=config.RESOURCE_OWNER_SECRET)

account_id = config.account_id
list_id = config.list_id
url = 'https://api.aweber.com/1.0/accounts/{}/lists/{}/subscribers/'.format(account_id, list_id)

#TODO: Figure out how to tackle pages of subscribers
try:
    x = 0
    while x < 500:
        response = aweber.get(url)
        entries = response.json()['entries']
        #print(response.json()['next_collection_link'])
        if response.json()['next_collection_link'] != ' ':
            for sub in entries:
                x += 1
                #print(str(x) + url)
                print(str(x) + ' ' + sub['email'])
                url = response.json()['next_collection_link']
        else:
            for sub in entries:
                x += 1
                print(x)
except Exception as e:
    print(e)
    
#TODO Code that places this information into a DB 
