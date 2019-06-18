from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import WishViewSet, WishlistView

urlpatterns = [
    path("user/<str:user_id>/", WishlistView.as_view()),
    path("", WishViewSet.as_view({'post': 'create'})),
    path("<int:pk>/", WishViewSet.as_view({'delete': 'delete'})),
]
