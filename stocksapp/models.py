from django.db import models
'''
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as gl
from django.utils import timezone
from datetime import datetime
import uuid
'''


###################################################
#               Managers                          #
###################################################
class StoreManager(models.Manager):
    def queryset(self):
        return super().get_queryset()

    def featured(self):
        return self.filter(is_featured=True, is_active=True) # self.get_queryset().filter(is_active=True, is_featured=True)

    def approved(self):
        return self.filter(is_active=True) # self.get_queryset().filter(is_approved=True)

    def active(self):
        return self.filter(is_active=True) # self.get_queryset().filter(is_active=True)



class Stock(models.Model):
    name = models.CharField(max_length=25)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'stocks'
