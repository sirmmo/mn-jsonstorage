from django.shortcuts import render

from django.http import HttpResponseForbidden
# Create your views here.

from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from core.models import *

import os

@csrf_exempt
def post_data(request,application,collection):
    auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
    if not auth:
        return HttpResponseForbidden()
    if Application.objects.filter(slug=application, secret=auth).count() == 0:
        return HttpResponseForbidden()
    if Collection.objects.filter(slug=collection, application__slug=application).count() == 0:
        return HttpResponseForbidden()
    
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    i = client[application][collection].insert_one(body)
    return HttpResponse(i.inserted_id)
        
def get_data(request,application,collection,ident):
    c = Collection.objects.get(slug=collection, application__slug=application)
    if c.private_get:
        auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
        if Application.objects.filter(slug=application, secret=auth).count() == 0:
            return HttpResponseForbidden()
            
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    data = client[application][collection].find_one({"_id":ObjectId(ident)}, {"_id":0})
    return HttpResponse(json.dumps(data))
        
def get_data_list(request, application, collection):
    c = Collection.objects.get(slug=collection, application__slug=application)
    if c.private_get:
        auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
        if Application.objects.filter(slug=application, secret=auth).count() == 0:
            return HttpResponseForbidden()
    
    if c.queryable:
        filters = json.loads(request.GET.get("filter"))
            
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    data = client[application][collection].find(filters, {"_id": 0})
    return HttpResponse(json.dumps(data))