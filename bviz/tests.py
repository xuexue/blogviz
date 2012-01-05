# Author : Jeeyoung Kim
from django.test import TestCase
from django.contrib.auth.models import User
from bviz.data_import import DataPuller
from pprint import pprint

LZ='34969445' # account_id for lisazhang.ca
class DataImportTest(TestCase):
  fixtures = ['auth.json']

  def setUp(self):
    self.user = User.objects.get(email='jeeyoungk@gmail.com')
    self.puller = DataPuller.from_user(self.user)

  def test_query_profiles(self):
    profiles = self.puller.query_profiles()
    assert profiles

  def test_top_pages(self):
    '''Query the most visited articles.'''
    result = self.puller.query(
        account_id=LZ,
        metrics='visits',
        dimensions=['pagePath','pageTitle'],
        sort='-visits',
        max_results=20)
    self.assertEquals(len(result['rows']), 20)

  def test_top_days(self):
    '''Query the days with top # of visitors. '''
    result = self.puller.query(
        account_id=LZ,
        metrics='visits',
        dimensions='date',
        sort='-visits',
        max_results=20)
    self.assertEquals(len(result['rows']), 20)

  def test_top_referral(self):
    result = self.puller.query(
        account_id=LZ,
        metrics='visits',
        dimensions=['source', 'referralPath'],
        sort='-visits',
        max_results=20)
    self.assertEquals(len(result['rows']), 20)

