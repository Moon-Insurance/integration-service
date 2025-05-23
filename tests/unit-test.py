import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Sale

class SalesServiceUnitTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_sale(self):
        response = self.app.post('/sales', json={
            'sale_id': 'S001', 'agent_id': 'A123', 'product': 'Life Insurance', 'amount': 1500.0
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['sale_id'], 'S001')

if __name__ == '__main__':
    unittest.main()
