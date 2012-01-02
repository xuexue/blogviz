from tornado.web import RequestHandler
import tornado.auth

class BaseHandler(RequestHandler):
  pass

class GoogleHandler(BaseHandler, tornado.auth.GoogleMixin):
  @tornado.web.asynchronous
  def get(self):
    if self.get_argument("openid.mode", None):
      # Authentication workflow finished - authenticate.
      self.get_authenticated_user(
        self.async_callback(self._on_auth)
      )
      return
    # Not authenticated - redirect to Google.
    self.authenticate_redirect()

  def _on_auth(self, user):
    self._auto_finish = True
    if not user:
      raise tornado.web.HTTPError(500, "Google auth failed")
    self.finish('authenticated')

