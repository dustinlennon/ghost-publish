
Setup
====

When setting up this directory, be sure to include an .env file

  GHOST_ADMIN_API_KEY=<ghost_admin_api_key>
  GHOST_PUBLISH_PATH=${HOME}/Workspace/repos/ghost-publish
  JUPYTER_DATA_DIR=/home/dnlennon/.local/share/jupyter
  PYTHONPATH=${GHOST_PUBLISH_PATH}:${GHOST_PUBLISH_PATH}/.venv/lib/python3.11/site-packages

and copy `~/Workspace/repos/vscode_repl.pth` file into the virtualenv site-packages directory.

This will ensure that pipenv has access to the shared jupyter libraries.

Create a symbolic link in `~/local/share/jupyter/nbconvert/templates` that links to the ghost template.
