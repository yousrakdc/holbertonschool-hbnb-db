import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json, request
import sys
import os

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the functions to test from the controllers module
from src.controllers.amenities import get_amenities, create_amenity, get_amenity_by_id, update_amenity, delete_amenity
from src.models.amenity import Amenity

app = Flask(__name__)

# Creating a test client
class AmenityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_amenities(self):
        with patch('src.controllers.amenities.Amenity.get_all') as mock_get_all:
            mock_get_all.return_value = [MagicMock(to_dict=lambda: {'id': '1', 'name': 'Pool'})]
            response = self.app.get('/amenities')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': '1', 'name': 'Pool'}])

    def test_create_amenity(self):
        with app.test_request_context('/amenities', method='POST', json={'name': 'Gym'}):
            with patch('src.controllers.amenities.Amenity.create') as mock_create:
                mock_create.return_value = MagicMock(to_dict=lambda: {'id': '2', 'name': 'Gym'})
                
                response = self.app.post('/amenities', json={'name': 'Gym'})
                
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json, {'id': '2', 'name': 'Gym'})

    def test_get_amenity_by_id(self):
        with patch('src.controllers.amenities.Amenity.get') as mock_get:
            mock_get.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Pool'})
            
            response = self.app.get('/amenities/1')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': '1', 'name': 'Pool'})

    def test_update_amenity(self):
        with app.test_request_context('/amenities/1', method='PUT', json={'name': 'Updated Pool'}):
            with patch('src.controllers.amenities.Amenity.update') as mock_update:
                mock_update.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Updated Pool'})
                
                response = self.app.put('/amenities/1', json={'name': 'Updated Pool'})
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'id': '1', 'name': 'Updated Pool'})

    def test_delete_amenity(self):
        with patch('src.controllers.amenities.Amenity.delete') as mock_delete:
            mock_delete.return_value = True
            
            response = self.app.delete('/amenities/1')
            
            self.assertEqual(response.status_code, 204)

    # Additional tests for error cases
    def test_create_amenity_missing_field(self):
        with app.test_request_context('/amenities', method='POST', json={}):
            with patch('src.controllers.amenities.Amenity.create') as mock_create:
                mock_create.side_effect = KeyError('name')
                
                response = self.app.post('/amenities', json={})
                
                self.assertEqual(response.status_code, 400)
                self.assertIn('Missing field: name', response.json['message'])

    def test_get_amenity_by_id_not_found(self):
        with patch('src.controllers.amenities.Amenity.get') as mock_get:
            mock_get.return_value = None
            
            response = self.app.get('/amenities/999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

    def test_update_amenity_not_found(self):
        with app.test_request_context('/amenities/999', method='PUT', json={'name': 'Nonexistent'}):
            with patch('src.controllers.amenities.Amenity.update') as mock_update:
                mock_update.return_value = None
                
                response = self.app.put('/amenities/999', json={'name': 'Nonexistent'})
                
                self.assertEqual(response.status_code, 404)
                self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

    def test_delete_amenity_not_found(self):
        with patch('src.controllers.amenities.Amenity.delete') as mock_delete:
            mock_delete.return_value = False
            
            response = self.app.delete('/amenities/999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json, request
import sys
import os

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the functions to test from the controllers module
from src.controllers.amenities import get_amenities, create_amenity, get_amenity_by_id, update_amenity, delete_amenity
from src.models.amenity import Amenity

app = Flask(__name__)

# Creating a test client
class AmenityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_amenities(self):
        with patch('src.controllers.amenities.Amenity.get_all') as mock_get_all:
            mock_get_all.return_value = [MagicMock(to_dict=lambda: {'id': '1', 'name': 'Pool'})]
            response = self.app.get('/amenities')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': '1', 'name': 'Pool'}])

    def test_create_amenity(self):
        with app.test_request_context('/amenities', method='POST', json={'name': 'Gym'}):
            with patch('src.controllers.amenities.Amenity.create') as mock_create:
                mock_create.return_value = MagicMock(to_dict=lambda: {'id': '2', 'name': 'Gym'})
                
                response = self.app.post('/amenities', json={'name': 'Gym'})
                
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json, {'id': '2', 'name': 'Gym'})

    def test_get_amenity_by_id(self):
        with patch('src.controllers.amenities.Amenity.get') as mock_get:
            mock_get.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Pool'})
            
            response = self.app.get('/amenities/1')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': '1', 'name': 'Pool'})

    def test_update_amenity(self):
        with app.test_request_context('/amenities/1', method='PUT', json={'name': 'Updated Pool'}):
            with patch('src.controllers.amenities.Amenity.update') as mock_update:
                mock_update.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Updated Pool'})
                
                response = self.app.put('/amenities/1', json={'name': 'Updated Pool'})
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'id': '1', 'name': 'Updated Pool'})

    def test_delete_amenity(self):
        with patch('src.controllers.amenities.Amenity.delete') as mock_delete:
            mock_delete.return_value = True
            
            response = self.app.delete('/amenities/1')
            
            self.assertEqual(response.status_code, 204)

    # Additional tests for error cases
    def test_create_amenity_missing_field(self):
        with app.test_request_context('/amenities', method='POST', json={}):
            with patch('src.controllers.amenities.Amenity.create') as mock_create:
                mock_create.side_effect = KeyError('name')
                
                response = self.app.post('/amenities', json={})
                
                self.assertEqual(response.status_code, 400)
                self.assertIn('Missing field: name', response.json['message'])

    def test_get_amenity_by_id_not_found(self):
        with patch('src.controllers.amenities.Amenity.get') as mock_get:
            mock_get.return_value = None
            
            response = self.app.get('/amenities/999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

    def test_update_amenity_not_found(self):
        with app.test_request_context('/amenities/999', method='PUT', json={'name': 'Nonexistent'}):
            with patch('src.controllers.amenities.Amenity.update') as mock_update:
                mock_update.return_value = None
                
                response = self.app.put('/amenities/999', json={'name': 'Nonexistent'})
                
                self.assertEqual(response.status_code, 404)
                self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

    def test_delete_amenity_not_found(self):
        with patch('src.controllers.amenities.Amenity.delete') as mock_delete:
            mock_delete.return_value = False
            
            response = self.app.delete('/amenities/999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn('Amenity with ID 999 not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

