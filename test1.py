import json
import requests
from copy import copy

session = requests.Session()
XSRFH = {"accept": "application/json, text/plain, */*","accept-language": "fr","content-type": "application/json;charset=UTF-8","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1"}

# LOGIN
payload = {"email": "raphael.kern", "password": open('pwd', 'r').read().replace('\n', '')}
print(payload)
auth = session.post('https://ent.iledefrance.fr/auth/login', data = payload)
if 'login' in auth.url: exit('Failed to login.')

XSRFH["x-xsrf-token"] = auth.cookies["XSRF-TOKEN"]

# SEARCH STUDENTS
res = session.get('https://ent.iledefrance.fr/userbook/structures', headers = XSRFH)
structures = [{'id': e['id'], 'name': e['name'], 'UAI': e['UAI']} for e in res.json()]

struct_id = structures[1]['id'] # to test

res = session.get(f'https://ent.iledefrance.fr/userbook/search/criteria/{struct_id}/classes', headers = XSRFH)
classes = res.json()['classes']

class_id = classes[1]['id']

data = {"search": "", "types": ["User"],
        "structures": [struct_id], "classes": [class_id],
        "profiles": ["Student"], "functions": [], "mood": True}

res = session.post('https://ent.iledefrance.fr/communication/visible', data = json.dumps(data), headers = XSRFH)

students = [{'id': e['id'], 'name': e['displayName']} for e in res.json()['users']]

# SEARCH SCRAPBOOKS
res = session.get('https://ent.iledefrance.fr/scrapbook/list/all', headers = XSRFH)
scrapBooks = res.json() # /!\: "_id"

book_id = scrapBooks[0]['_id']
print(book_id)
res = session.get(f'https://ent.iledefrance.fr/scrapbook/get/{book_id}', headers = XSRFH)
scrapBook = res.json()

# DUPLICATE SRAPBOOK
data = {"application": "scrapbook", "resourceId": book_id}
res = session.post('https://ent.iledefrance.fr/archive/duplicate', data = json.dumps(data), headers = XSRFH)
new_book_id = res.json()['duplicateId']

# RENAME BOOK
data = {}
data['title'] = 'NEW TITLE'
data['subTitle'] = 'NEW SUBTITLE'

data['coverColor'] = scrapBook['coverColor']
data['icon'] = scrapBook['icon']
data['trashed'] = 0

res = session.put(f'https://ent.iledefrance.fr/scrapbook/{new_book_id}', data = json.dumps(data), headers = XSRFH)
if 'error' in res.json().keys(): exit('Failed to duplicate.')

# DONE
