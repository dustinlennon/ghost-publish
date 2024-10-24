#!/usr/bin/env -S PIPENV_PIPFILE=/home/dnlennon/Workspace/repos/ghost-publish/Pipfile pipenv run python3

import argparse
import re
import yaml
import io
from pathlib import Path


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("target")
  parser.add_argument("--prefix", default = "_")

  args = parser.parse_args()

  # set output file names
  target_name = f"{args.prefix}{args.target}"
  yaml_name = Path(target_name).with_suffix(".yaml")

  yaml_block_started = False
  yaml_data = {}
  yaml_io = io.StringIO()
  content = []
  with open(args.target) as f:
    for line in f.readlines():
      m = re.match("^---$", line)

      if m and yaml_block_started == False:
        yaml_block_started = True

      elif m and yaml_block_started == True:
        yaml_io.seek(0)
        yaml_block = yaml.load(yaml_io, yaml.BaseLoader)
        yaml_data.update( yaml_block )
        yaml_block_started = False

      elif yaml_block_started:
        yaml_io.write(line)

      else:
        content.append( line )

  with open(yaml_name, "w") as f:
    yaml.dump(yaml_data, f)

  with open(target_name, "w") as f:
    f.writelines(content)
