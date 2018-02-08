from django.shortcuts import render

from django.http import HttpResponseForbidden, HttpResponse
# Create your views here.

from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from core.models import *

import json

import os

@csrf_exempt
def post_data(request,application,collection):
    #auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
    #if not auth:
    #    return HttpResponseForbidden()
    #if Application.objects.filter(slug=application, secret=auth).count() == 0:
    #    return HttpResponseForbidden()
    #if Collection.objects.filter(slug=collection, application__slug=application).count() == 0:
    #    return HttpResponseForbidden()
    
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    db = client[application]
    cl = db[collection]
    
    i = cl.insert_one(body)
    
    return HttpResponse(json.dumps(str(i.inserted_id)))
        
def get_data(request,application,collection,ident):
    c = Collection.objects.get(slug=collection, application__slug=application)
    #if c.private_get:
    #    auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
    #    if Application.objects.filter(slug=application, secret=auth).count() == 0:
    #        return HttpResponseForbidden()
            
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    db = client[application]
    cl = db[collection]
    
    data = cl.find_one({"_id": ObjectId(ident)}, {"_id": 0})
    data["id"] = ident
    return HttpResponse(json.dumps(data))
        
def get_data_list(request, application, collection):
    c = Collection.objects.get(slug=collection, application__slug=application)
    #if c.private_get:
    #    auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
    #    if Application.objects.filter(slug=application, secret=auth).count() == 0:
    #        return HttpResponseForbidden()
    
    if c.queryable:
        filters = json.loads(request.GET.get("filter", "{}"))
    else:
        filters = {}
            
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    db = client[application]
    cl = db[collection]
    
    data = cl.find(filters)
    l_data = list(data)
    for d in l_data:
        d["id"] = str(d["_id"])
        del d["_id"]
    return HttpResponse(json.dumps(l_data))
    
def delete_data_list(request, application, collection):
    filters = json.loads(request.GET.get("filter", "{}"))
    #auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
    #if Application.objects.filter(slug=application, secret=auth).count() == 0:
    #    return HttpResponseForbidden()
        
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    db = client[application]
    cl = db[collection]
    
    print filters
    if "_id" in filters:
        filters["_id"] = ObjectId(filters["_id"])
    
    data = cl.remove(filters)
        
    return HttpResponse(json.dumps("OK"))