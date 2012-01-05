# Author : Jeeyoung Kim
# Ajax-endpoints.
import json
import logging
from itertools import imap

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bviz import models as m
from bviz.data_import import DataPuller
from bviz.decorators import post_only

def render_as_json(request, dictionary):
  # TODO - add flags.
  assert 'success' not in dictionary
  dictionary['success'] = True
  json_str = json.dumps(dictionary, indent=True)
  return HttpResponse(json_str, mimetype='application/json')

@login_required
def profile(request):
  user = request.user
  profiles = m.GaProfile.objects.filter(user=user)
  items = []
  for profile in profiles:
    items.append(profile.info)
  d = {
    'items':items
  }
  return render_as_json(request, d)

@login_required
@csrf_exempt
@post_only
def refresh_profile(request):
  puller = DataPuller.from_user(request.user)
  puller.save_profiles()
  d = {}
  return render_as_json(request, d)

@login_required
def query(request):
  '''Perform a query against Google Analytics server.'''
  user = request.user
  first = lambda x : x[0]
  second = lambda x: x[1]
  account_id = request.REQUEST.get('account_id')
  # retrieving result from google API is pretty slow.
  # so, we're using caching.
  cache_key = '%s:%s:%s' % ('query',user.pk,account_id)
  result = cache.get(cache_key)
  if result is None:
    logging.debug('cache miss')
    puller = DataPuller.from_user(user)
    result = puller.query(
        account_id, metrics='visits',
        dimensions=['date'])
    cache.set(cache_key, result, 3600)
  else:
    logging.debug('cache hit')
  rows = result['rows']
  dates = imap(first, rows)
  stats = map(int, imap(second, rows))
  dates = ['%s/%s/%s' % (x[4:6],x[6:8],x[0:4]) for x in dates]
  d = {
    'stats':stats,
    'dates':dates,
  }
  return render_as_json(request, d)
