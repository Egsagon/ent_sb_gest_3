import json
import requests

# AUTHENTIFICATION #

XSRFHEADERS = {"accept": "application/json, text/plain, */*","accept-language": "fr","content-type": "application/json;charset=UTF-8","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1"}

def login(usr, pwd) -> dict:
   # Log in the user.
   
   with requests.Session() as s:
      payload = {"email": usr, "password": pwd}
      r = s.post('https://ent.iledefrance.fr/auth/login', data = payload)
      
      if 'login' in r.url: exit('Failed to login - Prob wrong creds.')
      
      return s.cookies

# BAKE THE COOKIES

cookies = login('raphael.kern', open('pwd', 'r').read())

xsrf = cookies["XSRF-TOKEN"]
print(f'Aquired xsrf {xsrf}')

headers = XSRFHEADERS
headers["x-xsrf-token"] = xsrf

# SEARCH

session = requests.Session()

def submit(url, method = 'GET', data = None) -> any:
   # Submit a query
   
   global headers
   global session
   
   r = session.request(method,
                       url,
                       data = data,
                       headers = headers)
   
   return r

# r = submit('https://ent.iledefrance.fr/userbook/structures')
# structures = r.json()

r = session.get('https://ent.iledefrance.fr/userbook/structures', headers = headers)
print(r.text)
# print(structures)