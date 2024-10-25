import argparse
import os
import yaml
import json
import requests
from pathlib import Path
from ghost_publish.shared import date_from_yaml, get_token
from datetime import date

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("target")
  parser.add_argument("--prefix", default = "_")
  return parser.parse_args()

def main():
  args = get_args()

  # set output file names
  prefix_name = Path(f"{args.prefix}{args.target}")

  doc_name = Path(args.target).with_suffix(".html")
  yaml_name = Path(prefix_name).with_suffix(".yaml")
  status_name = Path(args.target).with_suffix(".status")

  with open(yaml_name) as f:
    yaml_data = yaml.load(f, yaml.Loader)
  
  post_title = yaml_data.get("title", "Untitled")
  post_date = date_from_yaml(
    yaml_data.get("date", date.today())
  ).strftime("%Y-%m-%dT%H:%M:%S.000Z")

  with open(doc_name) as f:
    content = f.read()

  # create the post
  post = {
    'title' : post_title,
    'html' : f"<!--kg-card-begin: html-->\n{content}\n<!--kg-card-end: html-->",
    'created_at' : post_date,
    'updated_at' : post_date,
    'published_at' : post_date,
    # 'status': "published"
  }

  ghost_admin_api_key = os.environ['GHOST_ADMIN_API_KEY']
  ghost_admin_api_url = os.environ['GHOST_ADMIN_API_URL']

  token = get_token(ghost_admin_api_key)

  r = requests.post(
    ghost_admin_api_url,
    headers = {
      'Authorization': 'Ghost {}'.format(token)
    },
    json = { 
      'posts': [ post ] 
    }
  )
  r.raise_for_status()

  with open(status_name, "w") as f:
    json.dump(r.json(), f)

if __name__ == '__main__':
  main()