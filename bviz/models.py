from django.db import models as m
from django.contrib.auth.models import User

# Create your models here.

class Account(m.Model):
  account_id = m.IntegerField(primary_key=True)
  user = m.ForeignKey(User)

