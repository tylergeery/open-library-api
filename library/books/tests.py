from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch


class BookTests(APITestCase):
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_requires_query(self):
        """
        Ensure that querying books requires a `q` query param
        """
        response = self.client.get("/books/", {})
        self.assertEquals(400, response.status_code)

    @patch('books.views.query_open_library')
    def test_book_query(self, query_open_library_mock):
        """
        Ensure that we can query for book items
        """
        api_books = [
            {
                "key": "/works/123",
                "title": "Where the red fern grows",
                "author_name": ["unknown"],
                "publisher": ["TH House", "Redyard"],
                "last_modified_i": 1560731671,
                "first_publish_year": "1991",
            },
            {
                "key": "/works/456",
                "title": "clifford the big red dog",
                "last_modified_i": 1560731621,
            }
        ]
        api_output = {"docs": api_books}
        query_open_library_mock.return_value = api_output

        response = self.client.get("/books/?q=red")
        books = response.json()

        self.assertEquals(200, response.status_code)
        self.assertEquals(2, len(books))
        self.assertEquals(books[0]["id"], "123")
        query_open_library_mock.assert_called_with("search.json?q=red")

    @patch('books.views.query_open_library')
    def test_book_detail(self, query_open_library_mock):
        """
        Ensure that we can get details for a single book
        """
        api_book = {
            "key": "/works/123",
            "title": "Where the red fern grows",
            "subjects": ["kids", "tears"],
            "last_modified": {
                "value": "2009-12-10T21:29:26.680289",
            },
            "created": {
                "value": "2009-12-10T21:29:26.680289",
            }
        }
        query_open_library_mock.return_value = api_book

        response = self.client.get("/books/123/")
        book = response.json()

        self.assertEquals(200, response.status_code)
        self.assertEquals(book["id"], "123")
        query_open_library_mock.assert_called_with("/works/123.json")
