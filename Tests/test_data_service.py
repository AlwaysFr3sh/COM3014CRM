import unittest
import requests

url = "http://127.0.0.1:5001"
test_collection = "test_collection"

class TestDataService(unittest.TestCase):
  def test_CRUD(self):
    test_data = {"test" : "testing"}

    # Test create
    test_post = requests.post(f"{url}/create_entry/{test_collection}", json=test_data)
    entry_id = test_post.json()['id']

    print(entry_id)

    with self.subTest():
      self.assertEqual(test_post.status_code, 201)

    # test read
    test_get = requests.get(f"{url}/get_entry/{test_collection}/{entry_id}")
    test_get_data_without_id = test_get.json()
    test_get_data_without_id.pop("_id")
    with self.subTest():
      self.assertEqual(test_get_data_without_id, test_data)
    
    # test delete
    test_delete = requests.delete(f"{url}/delete_entry/{test_collection}/{entry_id}")
    with self.subTest():
      self.assertEqual(test_delete.status_code, 201)


if __name__ == "__main__":
  unittest.main()