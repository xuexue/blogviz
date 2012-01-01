from pprint import pprint

import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

import const


class Manager(object):
  def __init__(self):
    FLOW = OAuth2WebServerFlow(client_id=const.CLIENT_ID,
        client_secret=const.CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/analytics.readonly',
        user_agent='analytics-api-v3-awesomeness')

    TOKEN_FILE_NAME = 'analytics.dat'

    storage = Storage(TOKEN_FILE_NAME)
    credentials = storage.get()
    if not credentials or credentials.invalid:
      # Get a new token.
      credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)
    self.service = build('analytics', 'v3', http=http)

  def all_profiles(self):
    profile_list = self.service.management().profiles().list(accountId='~all',webPropertyId='~all').execute()
    return profile_list

  def data_get(self, account_id):
    '''import all data'''
    results = self.service.data().ga().get(
        ids=account_id,start_date='2011-01-01',
        end_date='2011-12-31',
        metrics='ga:visits',
        dimensions='ga:month').execute()
    return results


# accounts_list = service.management().accounts().list().execute()
# webproperties_list = service.management().webproperties().list(accountId='~all').execute()

if __name__ == '__main__':
  mgr = Manager()
  profiles = mgr.all_profiles()
  accountIds = []
  for item in profiles['items']:
    key = item['id']
    res = mgr.data_get('ga:%s'%key)
    print item['name'], key
    pprint(res['rows'])
