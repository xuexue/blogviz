from django.contrib.auth.models import User
from django.db import models as m
from social_auth.fields import JSONField

# Create your models here.

class GaProfile(m.Model):
  ''' A google analytics profile. '''
  account_id = m.IntegerField()
  profile_id = m.IntegerField()
  user = m.ForeignKey(User)
  info = JSONField()
