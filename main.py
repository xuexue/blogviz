#!/usr/bin/env python
import logging
import os.path

import tornado.ioloop
import tornado.web
from tornado.options import define, options

import handlers


def _define():
  define('port', 8080, int)
  define('debug', True, bool)

def get_app():
  root_dir = os.path.dirname(__file__)
  settings = {
    # Required settings
    'debug':options.debug,
    'template_path':os.path.join(root_dir, 'templates'),
    'static_path':os.path.join(root_dir, 'static'),
    'cookie_secret':'1234567890',
    'ui_modules':[],
  }
  hdlrs = [
  ]
  return tornado.web.Application(hdlrs, **settings)

def main():
  _define()
  application = get_app()
  application.listen(options.port)
  logging.info('Starting server on port %d', options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()

