from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class Application(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    
    secret = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.name
        
class Collection(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    
    private_get = models.BooleanField(default=True)
    queryable = models.BooleanField(default=False)
    exportable = models.BooleanField(default=False)
    
    schema = models.TextField(null=True, blank=True)
    force_validate = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    