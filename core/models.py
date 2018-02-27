from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
import uuid

# Create your models here.

class Application(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    
    secret = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.name
        
class Collection(models.Model):
    application = models.ForeignKey(Application, related_name="collections")
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    
    private_get = models.BooleanField(default=True)
    queryable = models.BooleanField(default=False)
    exportable = models.BooleanField(default=False)
    
    schema = models.TextField(null=True, blank=True)
    force_validate = models.BooleanField(default=False)
    
    custom_describe = models.BooleanField(default=False)
    custom_describe_json = models.TextField(null=True, blank=True)
    
    custom_describe_list = models.BooleanField(default=False)
    custom_describe_list_json = models.TextField(null=True, blank=True)
    
    is_geographic = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_geographic:
            server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
            port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
            
            client = MongoClient(host=server, port=int(port), connect=True)
            
            db = client[application]
            cl = db[collection]
            cl.create_index({"geometry":"2dsphere"})
        super(Collection, self).save(*args, **kwargs)
        