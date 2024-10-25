from nbconvert.preprocessors import ExtractOutputPreprocessor
from traitlets import Unicode
import re

class RegexSubPreprocessor(ExtractOutputPreprocessor):
  pattern = Unicode("").tag(config=True)
  repl = Unicode("").tag(config=True)

  def preprocess_cell(self, cell, resources, cell_index):    
    src : str = cell['source']
    
    lines = list()
    for line in src.splitlines():
      line = re.sub(self.pattern, self.repl, line)
      lines.append(line)

    cell['source'] = "\n".join(lines)

    return cell, resources


