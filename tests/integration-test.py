import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

class SalesServiceIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_crud(self):
        # Create
        res = self.client.post('/sales', json={'sale_id': 'S100', 'agent_id': 'A001', 'product': 'Health', 'amount': 2000})
        self.assertEqual(res.status_code, 201)

        # Read
        res = self.client.get('/sales/S100')
        data = res.get_json()
        self.assertEqual(data['product'], 'Health')

        # Update
        res = self.client.put('/sales/S100', json={'amount': 2500})
        data = res.get_json()
        self.assertEqual(data['amount'], 2500)

        # Delete
        res = self.client.delete('/sales/S100')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
