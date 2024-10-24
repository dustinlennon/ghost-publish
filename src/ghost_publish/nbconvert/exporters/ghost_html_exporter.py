from traitlets.config import Config, List, Unicode
from traitlets import log
from typing import Any
from nbconvert.exporters.html import HTMLExporter
# from nbconvert.preprocessors.extractoutput import ExtractOutputPreprocessor

# import ghost_publish
import os
from ghost_publish.shared import get_logger
from ghost_publish.nbconvert.preprocessors.extract_yaml import ExtractYamlPreprocessor
from ghost_publish.nbconvert.preprocessors.extract_output_link import ExtractOutputLinkPreprocessor
# from ghost_publish.preprocessors.output_md5 import OutputMd5Preprocessor
# from ghost_publish.preprocessors.regex_sub import RegexSubPreprocessor

class GhostHTMLExporter(HTMLExporter):

  template_name = "ghost"

  # ghost_admin_api_key = Unicode(allow_none = True).tag(config = True)
  # ghost_admin_api_url = Unicode(allow_none = True).tag(config = True)
  # output_files_dir = Unicode().tag(config = True)
  # a list of paths, each file containing a valid code injection.
  # code_injection_head_paths = List[Unicode]([]).tag(config = True)

  # disabled by default
  extra_preprocessors: List[Any] = List([
    "ghost_publish.nbconvert.preprocessors.regex_sub.RegexSubPreprocessor",
  ]).tag(config=True)

  # enabled by default
  preprocessors = List([
     ExtractYamlPreprocessor,
     ExtractOutputLinkPreprocessor
  ])

  def _init_preprocessors(self):
    """
    Seems to be the easiest way to extend the collection of preprocessors that behave like
    those in default_preprocessors.
    """
    super()._init_preprocessors()
    for preprocessor in self.extra_preprocessors:
      self.register_preprocessor(preprocessor)

  @property
  def default_config(self):
    c = Config(
      {
        "GhostHTMLExporter" : {
          "exclude_anchor_links" : True
        },
        "TagRemovePreprocessor": {
          "remove_cell_tags" : ['preamble', 'comment']
        },
        "RegexSubPreprocessor" : {
          'enabled' : True,
          'pattern' : "{icon=.*}"
        }
      }      
    )
    if super().default_config:
        c2 = super().default_config.copy()
        c2.merge(c)
        c = c2

    return c

  def _init_resources(self, resources):
    resources = super()._init_resources(resources)

    logger = log.get_logger()
    logger.debug(repr(resources))
    # ExtractOutputLinkPreprocessor uses this to set its default for output_files_dir
    resources['notebook_path'] = os.path.join(os.getcwd(), resources['metadata']['path'])

    return resources
