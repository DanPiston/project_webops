import sqlite3
import os
from requests_oauthlib import OAuth1Session
import config

aweber = OAuth1Session(client_key=config.CLIENT_KEY,
                       client_secret=config.CLIENT_SECRET,
                       resource_owner_key=config.RESOURCE_OWNER_KEY,
                       resource_owner_secret=config.RESOURCE_OWNER_SECRET)

account_id = config.account_id
list_id = config.list_id
url = 'https://api.aweber.com/1.0/accounts/{}/lists/{}/subscribers/'.format(account_id, list_id)

myfile = os.path.isfile('sub_db.db')
#create table if not present
if  myfile:
    for f in os.listdir():
        if f.endswith('.db'):
            os.unlink(f)
    conn = sqlite3.connect('sub_db.db')
    c = conn.cursor()
    c.execute(''' CREATE TABLE subs
                    (name text, email text, date_added text)''')
    conn.commit()
    conn.close()
conn = sqlite3.connect('sub_db.db')

while url:

    #connect to DB if present
    c = conn.cursor()
    sql = """ insert into subs values (
              :name, :email, :date)"""

    #Issue request to AWeber
    response = aweber.get(url)
    print('Status Code: ' + str(response.status_code))
    entries = response.json()['entries']
    for sub in entries:
        #add subscribers to sqlite db
        args = {
                'name':sub['name'],
                'email':sub['email'],
                'date':sub['subscribed_at']}
        c.execute(sql,args)
        conn.commit()
    if 'next_collection_link' in response.json().keys():
        url = response.json()['next_collection_link']
    else:
        url = None 



