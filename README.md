
ghost-publish
====

`ghost_publish` is a python package that provides scripts and nbconvert support to my [ghost blog](https://dlennon.org).  These tools facilitate access to the admin API, specifically when publishing posts.


setup
----

When setting things up, you'll likely need to set a few environment variables:

    <!-- GHOST_ADMIN_API_KEY=<ghost_admin_api_key>
    GHOST_ADMIN_API_URL=<ghost_admin_api_url> -->

    # PYTHONPATH includes the package source code and the site-packages; useful for external apps that might leverage a dotenv file.
    GHOST_PUBLISH_PATH=<this directory>
    PYTHONPATH=${GHOST_PUBLISH_PATH}/src:${GHOST_PUBLISH_PATH}/.venv/lib/python3.11/site-packages


Install the ghost-publish `PIPENV_VENV_IN_PROJECT=True pipenv install -e src`; uninstalling may require deleting the egg directory.


markdown support
----

If pandoc is installed, this should work out of the box.


jupyter notebook support
----

Install the ghost templates in a jupyter "data" path:

```bash
package_dir=$(pwd)
template_dir=$(jupyter --data-dir)/nbconvert/templates/ghost
mkdir -p $template_dir
ln -s \
    ${package_dir}/src/ghost_publish/nbconvert/templates/ghost/ghost.html.j2 \
    ${template_dir}/ghost.html.j2
ln -s \
    ${package_dir}/src/ghost_publish/nbconvert/templates/ghost/index.html.j2 \
    ${template_dir}/index.html.j2
```
