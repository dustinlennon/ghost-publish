import argparse
import re
import yaml
from pathlib import Path

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("target")
  parser.add_argument("--prefix", default = "_")
  return parser.parse_args()

def main():
  args = get_args()

  # set output file names
  target_name = f"{args.prefix}{args.target}"
  yaml_name = Path(target_name).with_suffix(".yaml")

  yaml_block_started = False
  yaml_data = {}
  yaml_content = []
  doc_content = []
  with open(args.target) as f:
    for line in f.readlines():
      m = re.match("^---$", line)

      if m and yaml_block_started == False:
        yaml_block_started = True

      elif m and yaml_block_started == True:
        yaml_content = "".join(yaml_content)
        yaml_block = yaml.load(yaml_content, yaml.BaseLoader)
        yaml_data.update( yaml_block )
        yaml_block_started = False

      elif yaml_block_started:
        yaml_content.append(line)

      else:
        doc_content.append( line )

  with open(yaml_name, "w") as f:
    yaml.dump(yaml_data, f)

  with open(target_name, "w") as f:
    f.writelines(doc_content)

if __name__ == '__main__':
  main()
