import requests
import os
from pathlib import Path
from slugify import slugify
import urllib.request 
import time
import json
import random
import calendar

# according to https://api.sketchfab.com/v3/licenses
ALLOWED_LICENSES = {'322a749bcfa841b29dff1e8a1bb74b0b', 'b9ddc40b93e34cdca1fc152f39b9f375', '72360ff1740d419791934298b8b6d270', 'bbfe3f7dbcdd4122b966b85b9786a989', '2628dbe5140a4e9592126c8df566c0b7', '34b725081a6a4184957efaec2cb84ed3', '7c23a1ba438d4306920229c12afcb5f9'}

DEST_PATH = os.environ['SKETCHFAB_DEST_PATH']
headers = {   
    'Authorization': 'Token '+os.environ['SKETCHFAB_API_TOKEN'],
}

params = {
    'categories' : 'cultural-heritage-history',
    'downloadable': 'true',
    'archives_flavours': 'false',
    'sort_by': 'createdAt',
    'cursor': None
}

print('Starting at', params['cursor'])
r = requests.get('https://api.sketchfab.com/v3/models', params=params, headers=headers)
i = 0
while True:
    data = r.json()
    for model in data['results']:
        if not model['license']['uid'] in ALLOWED_LICENSES:
            print('Skipping due to license', model['uid'])
            continue
        subpath = DEST_PATH+model['uid'][0:1]
        if Path(subpath+'/'+model['uid']+'.glb').is_file():
            print('Skipping because existing', model['uid'])
            continue
        Path(subpath).mkdir(exist_ok=True)
        with open(subpath+'/'+model['uid']+'.m.'+slugify(model['name'])+'.json', 'w') as json_file:
            json.dump(model, json_file)
        if model['thumbnails'] and len(model['thumbnails']['images']) > 0:
            urllib.request.urlretrieve(model['thumbnails']['images'][0]['url'], subpath+'/'+model['uid']+'.thumb.jpeg')
        f = requests.get('https://api.sketchfab.com/v3/models/'+model['uid']+'/download', headers=headers)
        files = f.json()
        if not 'glb' in files:
            print(f)
            print(files)
            print("MISSING", model['uid'])
            raise Exception("429?")
        #urllib.request.urlretrieve(files['source']['url'], subpath+'/'+model['uid']+'.zip')
        local_filename, resp_headers = urllib.request.urlretrieve(files['glb']['url'], subpath+'/'+model['uid']+'.glb')
        if 'Last-Modified' in resp_headers:
            mtime = calendar.timegm(time.strptime(resp_headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT'))
            os.utime(local_filename, (mtime, mtime))
        print('Completed:', i, 'Last:', model['uid'])
        i += 1
        time.sleep(random.randint(1,10))
    if not 'next' in data or not data['next']:
        break
    time.sleep(random.randint(1,4))
    print("Cursor:", data['cursors']['next'])
    r = requests.get(data['next'], headers=headers)

print("Done.")