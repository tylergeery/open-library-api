from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = ("id", "library_user_id", "book_id", "created_at", "updated_at")

    def get_validation_exclusions(self):
        exclusions = super(WishlistSerializer, self).get_validation_exclusions()
        return exclusions + ["created_at", "updated_at"]