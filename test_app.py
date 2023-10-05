import unittest
import warnings
from application import app, db, Drink
class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello World')

    def test_get_drinks(self):
        drink = Drink(name='Sample Drink', description='Test Description')
        db.session.add(drink)
        db.session.commit()

        response = self.app.get('/drinks')
        self.assertEqual(response.status_code, 200)
        self.assertIn('drinks', response.data.decode('utf-8'))
        self.assertIn('Sample Drink', response.data.decode('utf-8'))
        self.assertIn('Test Description', response.data.decode('utf-8'))

    def test_get_nonexistent_drink(self):
        with warnings.catch_warnings():  
            warnings.filterwarnings("ignore", category=Warning)  
            response = self.app.get('/drinks/1')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.data.decode('utf-8'))

    def test_add_drink(self):
        data = {'name': 'New Drink', 'description': 'New Description'}
        response = self.app.post('/drinks', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data.decode('utf-8'))

    def test_delete_drink(self):
        drink = Drink(name='Sample Drink', description='Test Description')
        db.session.add(drink)
        db.session.commit()

        response = self.app.delete('/drinks/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data.decode('utf-8'))

    def test_update_drink(self):
        drink = Drink(name='Sample Drink', description='Test Description')
        db.session.add(drink)
        db.session.commit()

        data = {'name': 'Updated Drink', 'description': 'Updated Description'}
        response = self.app.put('/drinks/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Message', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()

