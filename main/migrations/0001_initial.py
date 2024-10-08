# Generated by Django 4.2 on 2023-05-21 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Album Slug", unique=True)),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Albums",
                "db_table": "Albums",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Artist",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Artist Slug", unique=True)),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "album",
                    models.ManyToManyField(
                        related_name="artist_album", to="main.album"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Artists",
                "db_table": "Artists",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Category Slug", unique=True)),
                ("description", models.TextField()),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "meta_keywords",
                    models.CharField(
                        help_text="SEO keywords for meta tag",
                        max_length=255,
                        verbose_name="Meta Keywords",
                    ),
                ),
                (
                    "meta_description",
                    models.CharField(
                        help_text="Content for description meta tag",
                        max_length=255,
                        verbose_name="Meta Description",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "db_table": "categories",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Track",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Track Slug", unique=True)),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "albums",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album_tracks",
                        to="main.album",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.artist"
                    ),
                ),
                (
                    "features",
                    models.ManyToManyField(
                        related_name="artist_featured", to="main.artist"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Tracks",
                "db_table": "Tracks",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Playlist",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Playlist Slug", unique=True)),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("albums", models.ManyToManyField(to="main.album")),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.artist"
                    ),
                ),
                ("tracks", models.ManyToManyField(to="main.track")),
            ],
            options={
                "verbose_name_plural": "Playlists",
                "db_table": "Playlsits",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Chart",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(help_text="Playlist Slug", unique=True)),
                ("image_link", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("albums", models.ManyToManyField(to="main.album")),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.artist"
                    ),
                ),
                (
                    "tracks",
                    models.ManyToManyField(
                        related_name="chart_tracks", to="main.track"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="artist",
            name="tracks",
            field=models.ManyToManyField(
                related_name="artists_tracks", to="main.track"
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="album_artist",
                to="main.artist",
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="features",
            field=models.ManyToManyField(
                related_name="album_features", to="main.artist"
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="album_track",
                to="main.track",
            ),
        ),
    ]
