from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("books", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=True
                    ),
                ),
                ("library_user_id", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("book_id", models.CharField(max_length=100)),
            ],
        )
    ]
