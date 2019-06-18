from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Wishlist
from .serializers import WishlistSerializer

from rest_framework.authentication import BasicAuthentication

class WishViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def delete(self, request, pk: int):
        return self.destroy(self, request, pk=pk)


class WishlistView(APIView):
    queryset = Wishlist.objects.all().order_by('-created_at')
    serializer_class = WishlistSerializer

    def get(self, request, user_id):
        queryset = self.queryset.filter(library_user_id=user_id)
        serializer = WishlistSerializer(queryset, many=True)

        return Response(serializer.data)

