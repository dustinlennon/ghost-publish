from nbconvert.preprocessors import ExtractOutputPreprocessor
from datetime import datetime as date
from ghost_publish.shared import date_from_yaml
import yaml
import re

class ExtractYamlPreprocessor(ExtractOutputPreprocessor):

  def preprocess(self, nb, resources):
    resources["yaml_header"] = dict()
    resources["yaml_cells"] = set()

    for index, cell in enumerate(nb.cells):
      nb.cells[index], resources = self.preprocess_cell(cell, resources, index)

    nb.cells = [ c for i,c in enumerate(nb.cells) if i not in resources['yaml_cells'] ]
    resources.pop('yaml_cells')

    resources['post_title'] = resources['yaml_header'].get("title", "Untitled")
    resources['post_date']  = date_from_yaml(
      resources['yaml_header'].get("date", date.today())
    )
    
    return nb, resources

  def preprocess_cell(self, cell, resources, cell_index):    
    if cell['cell_type'] == "raw" and cell_index == 0:
      src = cell['source']

      m = re.match(r"^---(\n.*)\n---$", src, re.DOTALL)

      try:
        content = m.group(1)
        resources['yaml_header'].update(yaml.load(content, yaml.BaseLoader))
        resources['yaml_cells'].add(cell_index)

      except AttributeError:
        pass

    return cell, resources
  