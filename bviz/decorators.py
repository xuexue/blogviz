# Author : Jeeyoung Kim
# useful decorators.
from functools import wraps

########################################
# Decorators for request handlers.
def post_only(handler):
  @wraps(handler)
  def inner(request, *args, **kwargs):
    if request.method != 'POST':
      # TODO - figure out the right type of exception to throw in this situation.
      raise Exception, 'POST only.'
    return handler(request, *args, **kwargs)
  return inner

########################################
# Generic decorators.
