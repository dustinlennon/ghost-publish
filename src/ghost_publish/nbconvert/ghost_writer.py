import requests
from nbconvert.writers import WriterBase
from ghost_publish.shared import get_token

class GhostWriter(WriterBase):

  def write(self, output, resources, **kw):

    post_title = resources['post_title']
    post_date = resources['post_date'].strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # create the post
    post = {
      # 'slug' : make_slug(post_title),  # non-uniqueness seemed problematic here
      'title' : post_title,
      'html' : f"<!--kg-card-begin: html-->\n{output}\n<!--kg-card-end: html-->",
      'created_at' : post_date,
      'updated_at' : post_date,
      'published_at' : post_date,
      'status': "published"
    }

    code_injection_head_paths = resources['code_injection_head_paths']
    if code_injection_head_paths:
      content = []
      for path in code_injection_head_paths:
        with open(path, "r") as f:
          injection = f.read()
          content.append(injection)
      
      post['codeinjection_head'] = "\n\n".join(content)

    ghost_admin_api_key = resources['ghost_admin_api_key']
    ghost_admin_api_url = resources['ghost_admin_api_url']

    token = get_token(ghost_admin_api_key) 

    # print(json.dumps(post, indent=2))

    r = requests.post(
      ghost_admin_api_url,
      headers = {
        'Authorization': 'Ghost {}'.format(token)
      },
      json = { 
        'posts': [ post ] 
      }
    )
    r.raise_for_status()

