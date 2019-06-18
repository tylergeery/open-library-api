from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=1000)),
                ("authors", models.CharField(max_length=400)),
                ("publishers", models.CharField(max_length=5000)),
                ("last_modified_at", models.DateTimeField()),
                ("first_publish_year", models.CharField(max_length=4)),
            ],
        )
    ]
