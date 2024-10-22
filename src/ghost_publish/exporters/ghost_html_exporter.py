from traitlets.config import Config, List, Unicode
from typing import Any
from nbconvert.exporters.html import HTMLExporter

# import ghost_publish
import os
from ghost_publish.shared import get_logger
# from ghost_publish.preprocessors.output_md5 import OutputMd5Preprocessor
from ghost_publish.preprocessors.extract_yaml import ExtractYamlPreprocessor
# from ghost_publish.preprocessors.regex_sub import RegexSubPreprocessor

class GhostHTMLExporter(HTMLExporter):

  template_name = "ghost"

  ghost_admin_api_key = Unicode(allow_name = True).tag(config = True)
  ghost_admin_api_url = Unicode(allow_name = True).tag(config = True)

  # a list of paths, each file containing a valid code injection.
  code_injection_head_paths = List[Unicode]([]).tag(config = True)

  # disabled by default
  extra_preprocessors: List[Any] = List([
    "ghost_publish.preprocessors.regex_sub.RegexSubPreprocessor",
    "ghost_publish.preprocessors.output_md5.OutputMd5Preprocessor"
  ]).tag(config=True)

  # enabled by default
  preprocessors = List([
     ExtractYamlPreprocessor     
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
    resources['ghost_admin_api_key'] = self.ghost_admin_api_key or os.environ['GHOST_ADMIN_API_KEY']
    resources['ghost_admin_api_url'] = self.ghost_admin_api_url or os.environ['GHOST_ADMIN_API_URL']
    resources['code_injection_head_paths'] = [p for p in self.code_injection_head_paths if len(p) > 0]

    return resources
