import sys, os
import logging
import re
from typing import Any
from traitlets import log

import jwt
import datetime

def get_logger() -> (logging.Logger | logging.LoggerAdapter[Any]):
  """
  Import a logger and send it to stdout.  Note, the client code will need to set
  the log level.
  """
  logger = log.get_logger()

  handler_names = [ handler.get_name() for handler in logger.handlers ]
  if __name__ not in handler_names:
    handler = logging.StreamHandler(sys.stdout)
    handler.set_name(__name__)
    logger.addHandler(handler)

  return logger


def get_token(ghost_admin_api_key = None):
  if ghost_admin_api_key is None:
    ghost_admin_api_key = os.environ['GHOST_ADMIN_API_KEY']

  # Split the key into ID and SECRET
  id, secret = ghost_admin_api_key.split(':')

  # Prepare header and payload
  iat = int(datetime.datetime.now().timestamp())

  header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
  payload = {
      'iat': iat,
      'exp': iat + 5 * 60,
      'aud': '/admin/'
  }

  # Create the token (including decoding secret)
  token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

  return token


def date_from_yaml(obj):
  if isinstance(obj, datetime.date):
    return obj
  
  dt = datetime.datetime.fromisoformat(obj)
  return dt.date()


def make_slug(title : str):
  slug = re.sub(
    r"[^a-z0-9 -]",
    "",
    title.lower()
  )
  slug = re.sub("\W+", "-", slug)
  return slug