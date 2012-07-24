#!/usr/bin/env python
# Script to import data from Google Analytics.

# Refer to the page
# http://code.google.com/apis/explorer/
# For more informations.
import datetime
from pprint import pprint

import httplib2
import oauth2client.client # gdata client.
import social_auth.models
from apiclient.discovery import build
from django.conf import settings
from django.contrib.auth.models import User

from bviz import models as m


FMT = '%Y-%m-%d'
strptime = datetime.datetime.strptime

class DataPuller(object):
  def __init__(self, credentials, user=None,
      start_date=None,
      end_date=None):
    self.credentials = credentials
    # initialize HTTP client.
    http = httplib2.Http()
    http = credentials.authorize(http)

    self.service = build('analytics', 'v3', http=http)
    if start_date is None:
      self.start_date = strptime('2011-09-01', FMT)
    else:
      self.start_date = start_date
    if end_date is None:
      self.end_date = strptime('2011-12-31', FMT)
    else:
      self.end_date = end_date
    self.user = user

  @classmethod
  def from_user(cls, user, *args, **kwargs):
    '''Initiate an instance of DataPuller from an instance of Django.User.'''
    usa = social_auth.models.UserSocialAuth.objects.filter(
        user=user,
        provider='google-oauth2',
    ).get()
    cred = get_credentials(usa)
    puller = DataPuller(cred, user, *args, **kwargs)
    return puller

  ###
  # Query methods
  def query_profiles(self):
    profile_list = self.service.management().profiles().list(accountId='~all',webPropertyId='~all').execute()
    return profile_list['items']

  def query(self, account_id, metrics, dimensions, sort, **kwargs):
    '''
    Refer to 
      http://code.google.com/apis/analytics/docs/gdata/dimsmets/dimsmets.html
    for all the possible combinations of metrics and dimensions.
      http://code.google.com/apis/analytics/docs/gdata/v3/reference.html#q_summary
    for all the possible parameters.

    ga: prefix is automatically attached.
    '''
    prefix = lambda x : 'ga:%s' % x
    sort_prefix = lambda x : '-ga:%s' % x[1:] if x.startswith('-') else prefix(x)

    # convert the data accordingly.
    if not isinstance(metrics, basestring):
      metrics_query = ','.join(map(prefix, metrics))
    else:
      metrics_query = prefix(metrics)
    if not isinstance(dimensions, basestring):
      dimensions_query = ','.join(map(prefix, dimensions))
    else:
      dimensions_query = prefix(dimensions)
    if sort is not None:
      if not isinstance(sort, basestring):
        sort_query = ','.join(map(sort_prefix, sort))
      else:
        sort_query = sort_prefix(sort)
    else:
      sort_query=""
    if sort_query:
      kwargs['sort'] = sort_query
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

  ###
  # Saving methods.
  def save_profiles(self):
    assert self.user
    profiles = self.query_profiles()
    for profile in profiles:
      account_id = profile['accountId']
      profile_id = profile['id']
      info = profile
      obj, created = m.GaProfile.objects.get_or_create(
          user=self.user,
          profile_id = profile_id,
          account_id = account_id,
          defaults={'info':info}
      )
    return True

def get_credentials(user_social_auth):
  content = user_social_auth.extra_data
  token_expiry = None
  refresh_token=content['refresh_token']
  access_token=content['access_token']
  credentials = oauth2client.client.OAuth2Credentials(
    access_token=access_token,
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    refresh_token=refresh_token,
    token_expiry=token_expiry,
    token_uri="https://accounts.google.com/o/oauth2/token",
    user_agent='analytics-api-v3',
  )
  return credentials

class RedditAnalytics(object):
  def __init__(self, domain):
    self.domain = domain

def main():
  '''function for ad-hoc testing of functionality.'''
  user = User.objects.get(email='jeeyoungk@gmail.com')
  puller = DataPuller.from_user(user)
  # puller.save_profiles()
  for key in ['34969445']:
    result = puller.query_all(key,
        # metrics=['visits'],
        # dimensions=['pagePath','date','month','hour'],
        dimensions=['pagePath'],
        filter='',
    )
    pprint(result)
if __name__ == '__main__':
  main()
