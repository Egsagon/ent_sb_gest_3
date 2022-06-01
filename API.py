import json
import struct
import requests

HEAD = {"accept": "application/json, text/plain, */*","accept-language": "fr","content-type": "application/json;charset=UTF-8","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1"}

class Connection:
   def __init__(self, usr: str, pwd: str) -> None:
      '''
      Represents a connection to ENT.
      '''
      
      self.root = 'https://ent.iledefrance.fr'
      self.session = requests.Session()
      self.payload = {"email": usr, "password": str(pwd)}
      self.XSRF = {"accept": "application/json, text/plain, */*","accept-language": "fr","content-type": "application/json;charset=UTF-8","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1"}
      
      # Login
      auth = self.session.post('https://ent.iledefrance.fr/auth/login', data = self.payload)
      if 'login' in auth.url: exit('Failed to login.')
      
      self.XSRF["x-xsrf-token"] = auth.cookies["XSRF-TOKEN"]
      
   def getStructures(self) -> list:
      '''
      Gets the available structures.
      Returns a list containing dicts like: {'id', 'name'}
      '''
      
      res = self.session.get('https://ent.iledefrance.fr/userbook/structures', headers = self.XSRF)
      return [{'id': e['id'], 'name': e['name']} for e in res.json()]

   def getClasses(self, structure: dict) -> list:
      '''
      Gets the available classes for a structure.
      '''
      
      struct_id = structure['id']
      res = self.session.get(f'https://ent.iledefrance.fr/userbook/search/criteria/{struct_id}/classes', headers = self.XSRF)
      
      return res.json()['classes']
   
   def getStudents(self, structure: dict, classe: dict) -> list:
      '''
      Gets the available students for a classe.
      '''
      
      data = {"search": "", "types": ["User"],
        "structures": [structure['id']], "classes": [classe['id']],
        "profiles": ["Student"], "functions": [], "mood": True}

      res = self.session.post('https://ent.iledefrance.fr/communication/visible', data = json.dumps(data), headers = self.XSRF)

      return [{'id': e['id'], 'name': e['displayName']} for e in res.json()['users']]
   
   def makeFolder(self, name: str, contains: list = [], on: str = 'root') -> str:
      '''
      Creates a folder and returns its id.
      '''
      
      data = {"parentId": on, "title": name, "ressourceIds": contains}
      
      res = self.session.post(self.root + '/scrapbook/folder', data = json.dumps(data), headers = self.XSRF)
      
      return res.json()['_id']
   
   def getBooks(self) -> list:
      '''
      Gets all tha available books.
      '''
      
      res = self.session.get(self.root + '/scrapbook/list/all', headers = self.XSRF)
      return res.json() # /!\: "_id"
   
   def getBook(self, id: str) -> str:
      '''
      Gets data from a book given its _id (from self.getBooks).
      '''
      
      res = self.session.get(f'https://ent.iledefrance.fr/scrapbook/get/{id}', headers = self.XSRF)
      return res.json()
   
   def duplicateBook(self, id: str) -> str:
      '''
      Duplicates a book and returns its id.
      '''
      
      data = {"application": "scrapbook", "resourceId": id}
      res = self.session.post(self.root + '/archive/duplicate', data = json.dumps(data), headers = self.XSRF)
      return res.json()['duplicateId']
   
   def renameBook(self, id: str, name: str, subtitle: str) -> None:
      '''
      Renames a book.
      '''
      
      scrapBook = self.getBook(id)
      
      data = {}
      data['title'] = name
      data['subTitle'] = subtitle
      data['coverColor'] = scrapBook['coverColor']
      data['icon'] = scrapBook['icon']
      data['trashed'] = 0

      res = self.session.put(f'https://ent.iledefrance.fr/scrapbook/{id}', data = json.dumps(data), headers = self.XSRF)
      if 'error' in res.json().keys(): exit('Failed to duplicate.')


if __name__ == '__main__':
   
   client = Connection('raphael.kern', open('pwd', 'r').read().replace('\n', ''))
   
   '''
   # Get structures
   structures = client.getStructures()
   print([s['name'] for s in structures])
   index = int(input('Index: '))
   structure = structures[index]
   
   # Get classes
   classes = client.getClasses(structure)
   print([c['label'] for c in classes])
   index = int(input('Index: '))
   classe = classes[index]
   
   # Get students
   students = client.getStudents(structure, classe)
   
   print([s['name'] for s in students])
   '''
   
   books = client.getBooks()
   
   print([b['name'] for b in books])
   
   index = int(input('Index: '))
   
   book = books[index]
   
   book_data = client.getBook(book['_id'])
   
   
   '''
   newid = client.duplicateBook('d59bd113-c2d8-418a-939c-65027472cf11')
   
   client.renameBook(newid, 'RENAMED', 'Rrenamad')
   '''