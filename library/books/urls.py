from django.urls import path

from .views import BookDetailView, BooksView

urlpatterns = [
    path("", BooksView.as_view()),
    path("<str:id>/", BookDetailView.as_view()),
]
