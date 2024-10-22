# import logging
import sys, os
from typing import Optional
from pathlib import Path

import argparse
import nbformat

import json

from dataclasses import dataclass
# from traitlets import log
from traitlets.config import Config

from ghost_publish.exporters.ghost_html_exporter import GhostHTMLExporter
from ghost_publish.shared import get_logger, get_token

from nbconvert.writers.files import FilesWriter

import requests
# import jwt
from datetime import datetime as date


@dataclass
class ProgramArgs:
  notebook: str
  build: str
  _ghost_data_path: str
  ghost_admin_api_key: str
  post_title: Optional[str] = None
  post_date: Optional[str] = None
 
  @property
  def notebook_file(self):
    return f"{self.notebook}.ipynb"
  
  @property
  def prefix(self):
    if self.build == 'local':
      prefix = ""
    elif self.build == 'dev':
      prefix = "/"
    else:
      prefix = "https://dlennon.org/posts/"
    return prefix
 
  @property
  def build_path(self):
    return Path(self._ghost_data_path) / "staging/notebooks"
  
  @property
  def output_path(self):
    return Path("content/images/notebooks") / self.notebook

def get_program_args(supplied_args = None):
  parser = argparse.ArgumentParser(
    prog = "publish"
  )
  parser.add_argument("notebook")
  parser.add_argument("--build", choices = ['local', 'dev', 'prod'], default = 'local')
  parser.add_argument("--ghost-data-path", default = os.environ["GHOST_DATA_PATH"], dest = "_ghost_data_path")
  parser.add_argument("--ghost-admin-api-key", default = os.environ["GHOST_ADMIN_API_KEY"])
  parser.add_argument("--post-title")
  parser.add_argument("--post-date")

  args = parser.parse_args(supplied_args)
  return ProgramArgs(**vars(args))

def get_config(args : ProgramArgs):
  c = Config()
  c.OutputMd5Preprocessor.prefix = args.prefix
  c.FilesWriter.build_directory = str(args.build_path)

  return c

def process(config: Config, args : ProgramArgs):
  """
  Read the jupyter notebook, apply the GhostHTMLExporter exporter, write the HTML output.
  """
  # read the notebook
  with open(args.build_path / args.notebook_file, "r") as f:
    nbdata = f.read()
  nbjson = json.loads(nbdata)
  nb_content = nbformat.reads(nbdata, as_version = nbjson['nbformat'])

  # run the exporter
  exporter = GhostHTMLExporter(config = config)
  resources = {
     "output_files_dir" : str(args.output_path)
  }
  (body, resources) = exporter.from_notebook_node(nb_content, resources)

  # write the file
  writer = FilesWriter(config = config)
  writer.write(body, resources, notebook_name = args.notebook)

  return (body, resources)

def publish(config: Config, args : ProgramArgs, body, resources):
  # postprocess yaml header metadata
  header = resources['yaml_header']

  post_title = args.post_title or header['title']
  post_title = post_title.strip("'\"")

  post_date = args.post_date or header['date']
  post_date = date.fromisoformat(post_date).strftime("%Y-%m-%dT%H:%M:%S.000Z")

  # read the html file
  html_file = args.build_path / f"{args.notebook}.html"
  with open(html_file, "r") as f:
    html_data = f.read()

  # create the post
  post = {
    'title' : post_title,
    'html' : f"<!--kg-card-begin: html-->\n{html_data}\n<!--kg-card-end: html-->",
    'created_at' : post_date,
    'updated_at' : post_date,
    'published_at' : post_date,
    'status': "published"
  }

  # set up the call to the ghost admin api
  token = get_token(args.ghost_admin_api_key) 
  r = requests.post(
    'https://dlennon.org/posts/ghost/api/admin/posts/?source=html',
    headers = {
      'Authorization': 'Ghost {}'.format(token)
    },
    json = { 
      'posts': [ post ] 
    }
  )
  r.raise_for_status()


# def get_token(args : ProgramArgs):
#   # Split the key into ID and SECRET
#   id, secret = args.ghost_admin_api_key.split(':')

#   # Prepare header and payload
#   iat = int(date.now().timestamp())

#   header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
#   payload = {
#       'iat': iat,
#       'exp': iat + 5 * 60,
#       'aud': '/admin/'
#   }

#   # Create the token (including decoding secret)
#   token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

#   return token


if __name__ == '__main__':
  from ghost_publish.publish import *
  import shlex

  # logger = get_logger()
  # logger.setLevel(10)  

  # args = get_program_args(shlex.split("censoring"))
  args = get_program_args()
  config = get_config(args)

  print("\n".join(sys.path))
  print(repr(config))

  body, resources = process(config, args)

  if args.build == "local":
    sys.exit(0)

  publish(config, args, body, resources)

  # # delete post!
  # token = get_token(args) 
  # url = f"http://localhost:2368/ghost/api/admin/posts/{post_id}/"
  # headers = {'Authorization': 'Ghost {}'.format(token)}
  # body = {}
  # r = requests.delete(url, json=body, headers=headers)
