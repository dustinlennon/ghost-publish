from nbconvert.preprocessors import ExtractOutputPreprocessor
from traitlets import Unicode
import hashlib
import os
from traitlets import log

class ExtractOutputLinkPreprocessor(ExtractOutputPreprocessor):
  """
  The defaults extract outputs to the same location as the source document and
  write links with no path information.
  """

  output_files_dir = Unicode(allow_none = True).tag(config = True)
  link_path = Unicode("").tag(config = True)

  def preprocess(self, nb, resources):
    logger = log.get_logger()

    logger.debug(f"ExtractOutputLinkPreprocessor.output_files_dir: '{self.output_files_dir}'")
    if self.output_files_dir == "":
      self.output_files_dir = resources['notebook_path']
    # resources['output_files_dir'] = os.path.join(self.output_files_dir)
    resources['output_files_dir'] = self.output_files_dir
    logger.debug(f"resources['output_files_dir']: {resources['output_files_dir']}")

    nb, resources = super().preprocess(nb, resources)
    return nb, resources

  def relink(self, k):
    return os.path.join(self.link_path, os.path.basename(k))

  def preprocess_cell(self, cell, resources, cell_index):
    cell, resources = super().preprocess_cell(cell, resources, cell_index)

    for out in cell.get("outputs", []):
      if out.output_type in {"display_data", "execute_result"}:
        if 'filenames' in out.metadata:
          out.metadata['filenames'] = { k:self.relink(v) for k,v in out.metadata['filenames'].items() }

    return cell, resources
