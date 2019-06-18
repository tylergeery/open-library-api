from rest_framework.test import APIClient, APITestCase

class WishListTests(APITestCase):
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_create_wish_error(self):
        """
        Ensure the expected errors when bad requests are sent
        """
        cases = [
            {},
            {"book_id": "78sdafdsa"},
            {"library_user_id": 15},
        ]

        for req in cases:
            response = self.client.post("/wishlist/", req)
            self.assertEquals(400, response.status_code)

    def test_create_and_delete_wish_success(self):
        """
        Ensure that we can create a wishlist item "wish"
        """
        wish = {
            "book_id": "78sdafdsa",
            "library_user_id": 15
        }

        response = self.client.post("/wishlist/", wish)
        wish_created = response.json()

        self.assertEquals(201, response.status_code)
        self.assertTrue(wish_created["id"] > 0)

        response = self.client.delete(f"/wishlist/{wish_created['id']}/")
        self.assertEquals(204, response.status_code)

    def test_list_wishlist(self):
        """
        Ensure that we can accurately get a wishlist
        """
        wishes = [
            {
                "book_id": "78sdafdssdfsa",
                "library_user_id": 15
            },
            {
                "book_id": "78sdafdsa",
                "library_user_id": 15
            },
            {
                "book_id": "78sdafdsa",
                "library_user_id": 16
            },
        ]

        for wish in wishes:
            response = self.client.post("/wishlist/", wish)
            self.assertEquals(201, response.status_code)

        response = self.client.get(f"/wishlist/user/15/", wish)
        wishlist = response.json()
        wishlist_book_ids = [wish["book_id"] for wish in wishlist]
        intersection_ids = set(wishlist_book_ids).intersection({"78sdafdsa", "78sdafdssdfsa"})

        self.assertEquals(200, response.status_code)
        self.assertEquals(2, len(wishlist))
        self.assertEquals(2, len(intersection_ids))
