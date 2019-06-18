from django.db import models


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.CharField(max_length=100)
    library_user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["book_id", "library_user_id"]]

    def __str__(self):
        return f"Wishlist: {self.library_user_id} => {self.book_id} ({self.id})"
