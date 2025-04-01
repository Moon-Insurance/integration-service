import pytest
import os
import requests

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5003') 

# Sample test data
test_sale = {
    "sale_id": "S8001",
    "agent_id": "A7001",
    "product": "Smartphone",
    "amount": 799.99
}

@pytest.fixture(scope='function', autouse=True)
def cleanup_database():
    """Ensure cleanup after each test by deleting test sale."""
    yield  # Run the test first
    requests.delete(f"{BASE_URL}/{test_sale['sale_id']}")  # Cleanup after test execution

def test_create_sale():
    response = requests.post(f"{BASE_URL}/", json=test_sale)
    assert response.status_code == 201
    data = response.json()
    assert data['sale_id'] == test_sale['sale_id']

def test_get_sale():
    requests.post(f"{BASE_URL}/", json=test_sale)  # Insert data first
    response = requests.get(f"{BASE_URL}/{test_sale['sale_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data['sale_id'] == test_sale['sale_id']

def test_update_sale():
    requests.post(f"{BASE_URL}/", json=test_sale)  # Insert data first
    update_data = {"amount": 899.99}
    response = requests.put(f"{BASE_URL}/{test_sale['sale_id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == update_data['amount']

def test_delete_sale():
    requests.post(f"{BASE_URL}/", json=test_sale)  # Insert data first
    response = requests.delete(f"{BASE_URL}/{test_sale['sale_id']}")
    assert response.status_code == 200
    assert response.json()['message'] == 'Sale deleted'

    response = requests.get(f"{BASE_URL}/{test_sale['sale_id']}")  # Verify deletion
    assert response.status_code == 404
