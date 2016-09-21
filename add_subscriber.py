from requests_oauthlib import OAuth1Session
import time
from pprint import pprint
import config

def main():
    aweber = OAuth1Session(client_key=config.CLIENT_KEY,
                           client_secret=config.CLIENT_SECRET,
                           resource_owner_key=config.RESOURCE_OWNER_KEY,
                           resource_owner_secret=config.RESOURCE_OWNER_SECRET)

    account_id = config.account_id
    list_id = config.list_id
    url = 'https://api.aweber.com/1.0/accounts/{}/lists/{}/subscribers'.format(account_id, list_id)

    emails = ['danp+{}@gmail.com'.format(i) for i in range(500)]
    for email in emails:
        try:
            if add_sub(aweber, url, email, name='DanP'):
                print('Subscriber {} added to list {}'.format(email, list_id))
        except RateLimitException:
            print('Rate Limit Hit - Waiting 60 sec')
            time.sleep(60)
        except DuplicateSub:
            print('Email Already Subbed')
        except Exception as e:
            raise e


def add_sub(session, url, email, **kwargs):
    data = {'email': email,
            'ws.op': 'create'}
    data.update(kwargs)
    response = session.post(url, json=data)
    if response.status_code == 201:
        return True
    else:
        error = response.json()['error']['message']
        if error.startswith('Rate L'):
            raise RateLimitException 
        elif error.startswith('email: Sub'):
            raise DuplicateSub 
        else:
            raise Exception(response.status_code, error)


class RateLimitException(Exception):
    pass

class DuplicateSub(Exception):
    pass

if __name__ == "__main__":
    main()
