#!/usr/bin/env python
import datetime

import httplib2
import oauth2client.client # gdata client.
import social_auth.models
from apiclient.discovery import build
from django.conf import settings
from pprint import pprint

FMT = '%Y-%m-%d'
strptime = datetime.datetime.strptime

class DataPuller(object):
  '''
  '''
  def __init__(self, credentials):
    self.credentials = credentials
    # initialize HTTP client.
    http = httplib2.Http()
    http = credentials.authorize(http)

    self.service = build('analytics', 'v3', http=http)
    self.start_date = strptime('2011-01-01', FMT)
    self.end_date = strptime('2011-12-31', FMT)

  def all_profiles(self):
    profile_list = self.service.management().profiles().list(accountId='~all',webPropertyId='~all').execute()
    return profile_list

  def query(self, account_id, metrics, dimensions,
    **kwargs):
    '''
    Refer to 
    http://code.google.com/apis/analytics/docs/gdata/dimsmets/dimsmets.html
    for all the possible combinations of metrics and dimensions

    ga: prefix is automatically attached.
    '''
    prefix = lambda x : 'ga:%s' % x

    # convert the data accordingly.
    if not isinstance(metrics, basestring):
      metrics_query = ','.join(map(prefix, metrics))
    else:
      metrics_query = prefix(metrics)
    if not isinstance(dimensions, basestring):
      dimensions_query = ','.join(map(prefix, dimensions))
    else:
      dimensions_query = prefix(dimensions)
    ids = prefix(account_id)
    
    # actual call.
    results = self.service.data().ga().get(
        ids=ids,
        start_date=self.start_date.strftime(FMT),
        end_date=self.end_date.strftime(FMT),
        metrics=metrics_query,
        dimensions=dimensions_query,
        **kwargs
    ).execute()
    return results

  def query_all(self, account_id, metrics, dimensions, **kwargs):
    '''
    Repeatedly query GA for data, using pagination.
    '''
    max_results = 1000
    start_index = 1
    total_results = None
    rows = []
    while total_results is None or total_results >= start_index:
      # TODO - perform error checking.
      results = self.query(
          account_id, metrics, dimensions,
          max_results=max_results,start_index=start_index,
          **kwargs
      )
      total_results = results['totalResults']
      pprint(results)
      rows += results['rows']
      start_index += max_results
    return rows

def get_cred(user_social_auth):
  content = user_social_auth.extra_data
  token_expiry = None
  refresh_token=content['refresh_token']
  access_token=content['access_token']
  credentials = oauth2client.client.OAuth2Credentials(
    access_token=access_token,
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    refresh_token=refresh_token
    token_expiry=token_expiry,
    token_uri="https://accounts.google.com/o/oauth2/token",
    user_agent='analytics-api-v3',
  )
  return credentials

def main():
  usa = social_auth.models.UserSocialAuth.objects.filter(uid='jeeyoungk@gmail.com').get()
  cred = get_cred(usa)
  puller = DataPuller(cred)
  all_profiles = puller.all_profiles()
  # ids = [x['id'] for x in all_profiles['items']]
  # for key in ids:
  for key in ['34969445']:
    result = puller.query_all(key,
        metrics=['visits'],
        # dimensions=['pagePath','date','month','hour'],
        dimensions=['pagePath'],
        filter='',
    )
    pprint(result)


if __name__ == '__main__':
  main()
