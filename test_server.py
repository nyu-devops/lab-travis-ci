# Test cases can be run with any of the following:
# python -m unittest discover
# nosetests --verbosity 2
# nosetests --with-spec --spec-color
# coverage run --omit "venv/*" test_server.py
# coverage report -m --include= server.py
# nosetests --with-coverage --cover-package=server

import unittest
import json
import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Pet Model for demo
pet1 = {"name": "fido", "category": "dog"}
pet2 = {"name": "kitty", "category": "cat"}

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        self.app = server.app.test_client()
        server.init_redis('127.0.0.1', 6379, None)
        server.reset()
        server.data_load(pet1)
        server.data_load(pet2)

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue ('Pet Demo REST API Service' in resp.data)

    def test_get_pet_list(self):
        resp = self.app.get('/pets')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_pet(self):
        resp = self.app.get('/pets/2')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'kitty')

    def test_get_pet_not_found(self):
        resp = self.app.get('/pets/0')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

    def test_create_pet(self):
        # save the current number of pets for later comparrison
        pet_count = self.get_pet_count()
        # add a new pet
        new_pet = {"name": "sammy", "category": "snake"}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        # test results
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'sammy')
        # check that count has gone up
        resp = self.app.get('/pets')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == pet_count + 1 )

    # def test_create_existing_pet(self):
    #     new_pet = {'name': 'fido', 'kind': 'dog'}
    #     data = json.dumps(new_pet)
    #     resp = self.app.post('/pets', data=data, content_type='application/json')
    #     self.assertTrue( resp.status_code == HTTP_409_CONFLICT )

    def test_update_pet(self):
        pet = {}
        pet['name'] = "kitty"
        pet['category'] = "loin"
        data = json.dumps(pet)
        resp = self.app.put('/pets/2', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['category'] == 'loin')

    def test_update_pet_not_found(self):
        new_kitty = {"name": "timothy", "category": "mouse"}
        data = json.dumps(new_kitty)
        resp = self.app.put('/pets/0', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

    def test_delete_pet(self):
        # save the current number of pets for later comparrison
        pet_count = self.get_pet_count()
        # delete a pet
        resp = self.app.delete('/pets/2', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_pet_count()
        self.assertTrue ( new_count == pet_count - 1)

    def test_create_pet_with_no_name(self):
        new_pet = {"category": "dog"}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_query_pets(self):
        resp = self.app.get('/pets?category=dog')
        #print 'resp_data: ' + resp.data
        print resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        self.assertTrue( 'fido' in resp.data)
        self.assertFalse( 'kitty' in resp.data)


######################################################################
# Utility functions
######################################################################

    def get_pet_count(self):
        # save the current number of pets
        resp = self.app.get('/pets')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
