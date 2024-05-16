# Generated by Django 4.2 on 2023-05-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                ("symbol", models.CharField(max_length=10, unique=True)),
            ],
            options={
                "verbose_name_plural": "stocks",
            },
        ),
    ]
