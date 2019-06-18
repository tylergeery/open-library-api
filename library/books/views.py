import urllib.parse
from datetime import datetime
from typing import Any, Dict

import requests
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView


def query_open_library(api_endpoint: str) -> Dict[str, Any]:
    """
    Perform the HTTP request to retrieve books from OpenLibrary API
    """
    try:
        response = requests.get(f"http://openlibrary.org/{api_endpoint}", timeout=1.5)
        response.raise_for_status()
    except (requests.ConnectionError, requests.ConnectTimeout):
        raise LibraryAPIUnavailable
    except requests.HTTPError:
        raise NotFound(detail="OpenLibrary Resource does not exist")

    return response.json()


class LibraryAPIUnavailable(APIException):
    status_code = 503
    default_detail = "OpenLibrary temporarily unavailable, try again later."
    default_code = "library_api_unavailable"


class BooksView(APIView):
    @staticmethod
    def api_book_to_output_dict(api_book: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes an api_book object from the OpenLibrary API and returns an instance of Book
        """

        return {
            "id": api_book["key"].lstrip("/works/"),
            "title": api_book["title"],
            "authors": api_book.get("author_name", []),
            "publishers": api_book.get("publisher", []),
            "last_modified_at": datetime.utcfromtimestamp(api_book["last_modified_i"]),
            "first_publish_year": api_book.get("first_publish_year", ""),
        }

    def get(self, request):
        """
        Get a list of books that match a supplied query (query param `q`)

        These books will all be fetched from the Open Search API
        https://openlibrary.org/dev/docs/api/search
        """

        query = request.GET.get("q")

        if not query:
            return Response("query param 'q' is required", status=400)

        book_response = query_open_library(
            f"search.json?q={urllib.parse.quote_plus(query)}"
        )
        book_list = map(self.api_book_to_output_dict, book_response["docs"])

        return Response(book_list)


class BookDetailView(APIView):
    @staticmethod
    def api_book_to_output_dict(api_book: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes an api_book object from the OpenLibrary API and returns an instance of Book
        """

        return {
            "id": api_book["key"].lstrip("/works/"),
            "title": api_book["title"],
            "subjects": api_book.get("subjects", []),
            "last_modified_at": api_book["last_modified"]["value"],
            "created_at": api_book["created"]["value"],
        }

    def get(self, request, id: int) -> Response:
        """
        Get specific details about an OpenLibrary book
        """

        book_response = query_open_library(f"/works/{id}.json")

        return Response(self.api_book_to_output_dict(book_response))
