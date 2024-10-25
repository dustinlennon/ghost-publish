
ghost-publish
====

`ghost_publish` is a python package that provides scripts and nbconvert support to the Ghost blog.  These tools facilitate access to the admin API, specifically when publishing posts.


setup
----

When setting things up, you'll likely need to set a few environment variables:

  GHOST_ADMIN_API_KEY=<ghost_admin_api_key>
  GHOST_ADMIN_API_URL=<ghost_admin_api_url>

  # PYTHONPATH includes the package source code and the site-packages; useful for external apps that might leverage a dotenv file.
  GHOST_PUBLISH_PATH=<this directory>
  PYTHONPATH=${GHOST_PUBLISH_PATH}/src:${GHOST_PUBLISH_PATH}/.venv/lib/python3.11/site-packages

I have a shared jupyter / ipython installation on my dev machine that loads up dotenv files when available.  For those, as well as vscode, copying the `~/Workspace/vscode_repl.pth` file into the virtualenv site-packages directory means that these applications will augment PYTHONPATH accordingly.

    # vscode_repl.pth
    ${HOME}/.local/share/virtualenvs/python3.11-qW6omolQ/lib/python3.11/site-packages


Create a symbolic link in `${HOME}/local/share/jupyter/nbconvert/templates` that links to the ghost template.  You may also need to link `base` in the same subdirectory.

Install the ghost-publish `pipenv install -e src`; uninstalling may require deleting the egg directory.

