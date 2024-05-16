from django.db import models
from django.urls import reverse

#####################################
           #TRACKS#
#####################################

class SiteManager(models.Manager):

    def queryset(self):
        return super().get_queryset()

    def featured(self):
        return self.filter(is_featured=True, is_active=True)

    def approved(self):
        return self.filter(is_active=True)

    def active(self):
        return self.filter(is_active=True)


class Album(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True, help_text="Album Slug")
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='album_artist')
    features = models.ManyToManyField('Artist', related_name='album_features')
    #image = models.ImageField(upload_to='images/', null=False)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    track = models.ForeignKey('Track', related_name='album_track', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
        #return reverse("main:_", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'Albums'
        ordering = ['-created_at']
        verbose_name_plural = 'Albums'


class Artist(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True, help_text="Artist Slug")
    album = models.ManyToManyField('Album', related_name='artist_album')
    #image = models.ImageField(upload_to='images/', null=False)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    tracks = models.ManyToManyField('Track', related_name='artists_tracks')
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
        #return reverse("main:_", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'Artists'
        ordering = ['-created_at']
        verbose_name_plural = 'Artists'


class Playlist(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)    # ===>  Do User Later <=== #
    slug = models.SlugField(max_length=50, unique=True, help_text="Playlist Slug")
    albums = models.ManyToManyField('Album')
    #image = models.ImageField(upload_to='images/', null=False)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    tracks = models.ManyToManyField('Track')
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
        #return reverse("main:_", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'Playlsits'
        ordering = ['-created_at']
        verbose_name_plural = 'Playlists'

class Chart(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)    # ===>  Do User Later <=== #
    slug = models.SlugField(max_length=50, unique=True, help_text="Playlist Slug")
    albums = models.ManyToManyField('Album')
    #image = models.ImageField(upload_to='images/', null=False)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    tracks = models.ManyToManyField('Track', related_name='chart_tracks')
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

class Track(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True, help_text="Track Slug")
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    features = models.ManyToManyField('Artist', related_name='artist_featured')
    #image = models.ImageField(upload_to='images/', null=False)
    albums = models.ForeignKey('Album',related_name='album_tracks', on_delete=models.CASCADE, null=True)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:_", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'Tracks'
        ordering = ['-created_at']
        verbose_name_plural = 'Tracks'

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text="Category Slug")
    description = models.TextField()
    #image = models.ImageField(upload_to='images/', null=False)
    image_link = models.CharField(max_length=50, unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteManager()
    active = SiteManager().active
    featured = SiteManager().featured

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
        #return reverse("main:category", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

#####################################
           #Store#
#####################################


#####################################
           #Dashboard#
#####################################


#####################################
           #Blog#
#####################################