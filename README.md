
Setup
====

When setting up this directory, be sure to include an .env file

  GHOST_ADMIN_API_KEY=<ghost_admin_api_key>
  GHOST_DATA_PATH=${HOME}/Workspace/repos/ghost-data
  GHOST_PUBLISH_PATH=${HOME}/Workspace/repos/ghost-publish
  JUPYTER_DATA_DIR=/home/dnlennon/.local/share/jupyter
  PYTHONPATH=${GHOST_PUBLISH_PATH}/src:${GHOST_PUBLISH_PATH}/.venv/lib/python3.11/site-packages

and copy `~/Workspace/vscode_repl.pth` file into the virtualenv site-packages directory.  This will ensure that pipenv has access to the shared jupyter libraries.

Create a symbolic link in `~/local/share/jupyter/nbconvert/templates` that links to the ghost template.

Build the ghost-publish package.  `pipenv run python3 -m build src`.  This sets up the entry point for jupyter nbconvert.

Install an editable package `pipenv run pip install -e src`; uninstall by deleting the egg directory.

<!-- Running
====

As a script

```bash
pipenv run python3 -m ghost_publish.publish
```


From the command line

```bash
GHOST_DATA_PATH="/home/dnlennon/Workspace/repos/ghost-data" \
GHOST_ADMIN_API_URL="https://dlennon.org/posts/ghost/api/admin/posts/?source=html" \
  jupyter nbconvert \
  --to ghost \
  --Application.log_level=10 \
  --NbConvertApp.output_files_dir=${GHOST_DATA_PATH}/staging/notebooks \
  --NbConvertApp.writer_class=ghost_publish.ghost_writer.GhostWriter \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags=preamble \
  --TagRemovePreprocessor.remove_cell_tags=comment \
  --RegexSubPreprocessor.enabled=True \
  --RegexSubPreprocessor.pattern="\{icon=.*\}" \
  --GhostHTMLExporter.code_injection_head_paths=./resources/bpp_custom_tex.html \
  ${GHOST_DATA_PATH}/staging/notebooks/bayesian_point_processes.ipynb

```


### copy and paste

```bash
export NOTEBOOK="/home/dnlennon/Workspace/repos/ghost-data/staging/notebooks/hessenberg.ipynb"
GHOST_ADMIN_API_URL="https://dlennon.org/posts/ghost/api/admin/posts/?source=html" \
  jupyter nbconvert \
  --to ghost \
  --Application.log_level=10 \
  --NbConvertApp.writer_class=ghost_publish.ghost_writer.GhostWriter \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags=preamble \
  --TagRemovePreprocessor.remove_cell_tags=comment \
  --RegexSubPreprocessor.enabled=True \
  --RegexSubPreprocessor.pattern="\{icon=.*\}" \
  $NOTEBOOK

``` -->