# Author : Jeeyoung Kim
# Ajax-endpoints.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from bviz.data_import import DataPuller
from itertools import imap

from bviz import models as m

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
def query(request):
  '''Perform a query against Google Analytics server.'''
  user = request.user
  first = lambda x : x[0]
  second = lambda x: x[1]
  puller = DataPuller.from_user(user)
  account_id = request.REQUEST.get('account_id')
  result = puller.query(
      account_id, metrics='visits',
      dimensions=['date'])
  rows = result['rows']
  dates = imap(first, rows)
  stats = map(int, imap(second, rows))
  dates = ['%s/%s/%s' % (x[4:6],x[6:8],x[0:4]) for x in dates]
  d = {
      'stats':stats,
      'dates':dates,
  }
  return render_as_json(request, d)
