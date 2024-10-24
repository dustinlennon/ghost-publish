#!/usr/bin/env -S PIPENV_PIPFILE=/home/dnlennon/Workspace/repos/ghost-publish/Pipfile pipenv run python3
from pandocfilters import toJSONFilters, Image
import os
import hashlib

def prep_image(src, src_pth, rpath):
    rpath = rpath.removeprefix("/")

    src_file = os.path.join(src_pth, src)
    with open(src_file, "rb") as f:
      data = f.read()
      md5 = hashlib.md5(data).hexdigest()

    _, ext = os.path.splitext(src_file)

    dst_pth = os.path.join(src_pth, rpath)
    dst_file = os.path.join(dst_pth, f"{md5}{ext}")

    os.makedirs(dst_pth, exist_ok = True)
    with open(dst_file, "wb") as f:
        f.write(data)

    link_rpath = os.path.join(rpath, f"{md5}{ext}")

    return link_rpath

def action(key, value, format, meta):
    if key == 'Image':
      attr, caption, [src, title] = Image(*value)['c']
      src = prep_image(
         src,
         meta['src_pth']['c'],
         meta['rpath']['c']
        )
      return Image(attr, caption, [src, title])

def cleanup(key, value, format, meta):
   meta.pop("rpath", None)
   meta.pop("src_pth", None)

# def extract(key, value, format, meta):
#     if key in ['Image']:
#         T = getattr(pandocfilters, key)
#         v = T(*value)
#         meta.setdefault(key, list()).append(v)

# def dumpmeta(key, value, format, meta):
#     dumped = meta.setdefault('dumped', False)
#     if dumped == False:
#         # print(repr(meta), file = sys.stderr)
#         print(repr(meta['rpath']), file=sys.stderr)
#         print(repr(meta['src_pth']), file=sys.stderr)
#         meta['dumped'] = True
#     return None


if __name__ == '__main__':
  """
  pandoc --filter ~/Workspace/repos/ghost-publish/src/ghost_publish/pandoc/postprocess.py \
    --metadata=rpath:/foo/bar/20131001_olcp \
    --metadata=src_pth:$(pwd) \
    20131001_olcp.html
  
  """
  toJSONFilters([action, cleanup])
