from django.shortcuts import render

from django.http import HttpResponseForbidden, HttpResponse
# Create your views here.

from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from core.models import *

import json

import os
from django_eventstream import send_event

AUTHENTICATION = False

@csrf_exempt
def post_data(request,application,collection):
    if AUTHENTICATION:
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
    db = client[application]
    cl = db[collection]
    
    if "id" in body:
        old_id = body.get("id")
        cl.update_one({"_id":ObjectId(old_id)}, {"$set":{"__deleted__":True}}, upsert=True)
        body["__previous_id__"] = old_id
    
    i = cl.insert_one(body)
    
    body["id"] = str(body["_id"])
    del body["_id"]
    
    send_event(application, 'added', body)

    return HttpResponse(json.dumps(str(i.inserted_id)))
        
def get_data(request,application,collection,ident):
    c = Collection.objects.get(slug=collection, application__slug=application)
    if AUTHENTICATION:
        if c.private_get:
            auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
            if Application.objects.filter(slug=application, secret=auth).count() == 0:
                return HttpResponseForbidden()
            
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    db = client[application]
    cl = db[collection]
    
    data = cl.find_one({"_id": ObjectId(ident)}, {"_id": 0})
    data["id"] = ident
    
    data ["__versions__"] = []
    prev = data.get("__previous_id__")
    while prev:
        data ["__versions__"].append(prev)
        pitm = cl.find_one({"_id": ObjectId(prev)}, {"_id": 0})
        prev = pitm.get("__previous_id__")
    
    return HttpResponse(json.dumps(data))
        
def get_data_list(request, application, collection):
    c = Collection.objects.get(slug=collection, application__slug=application)
    if AUTHENTICATION:
        if c.private_get:
            auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
            if Application.objects.filter(slug=application, secret=auth).count() == 0:
                return HttpResponseForbidden()
    
    if c.queryable:
        filters = json.loads(request.GET.get("filter", "{}"))
    else:
        filters = {}
            
    filters["__deleted__"] = {"$exists":False}
    
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
    if c.is_geographic:
        l_data = {"type":"FeatureCollection", "features":l_data}
    else:
        return HttpResponse(json.dumps(l_data))
    
def delete_data_list(request, application, collection):
    filters = json.loads(request.GET.get("filter", "{}"))
    if AUTHENTICATION:
        auth = request.META.get("HTTP_MN_JSONSTORAGE_SECRET")
        if Application.objects.filter(slug=application, secret=auth).count() == 0:
            return HttpResponseForbidden()
        
    server = os.getenv("JSONSTORAGE_MONGODB_HOST", "localhost")
    port = os.getenv("JSONSTORAGE_MONGODB_PORT", "27017")
    
    client = MongoClient(host=server, port=int(port), connect=True)
    
    db = client[application]
    cl = db[collection]
    
    print filters
    if "_id" in filters:
        filters["_id"] = ObjectId(filters["_id"])
    
    data = cl.remove(filters)
    
    send_event(application, 'deleted', {})
        
    return HttpResponse(json.dumps("OK"))
    
def describe(request, application, collection):
    c = Collection.objects.get(slug=collection, application__slug=application)
    mode = request.GET.get("mode")
    if AUTHENTICATION:
        pass
    ret = ""
    if c.custom_describe:
        ret = json.loads(c.custom_describe_json)
    return HttpResponse(json.dumps(ret))
    

def describe_list(request, application, collection):
    mode = request.GET.get("mode")
    if AUTHENTICATION:
        pass
    return HttpResponse(json.dumps())
    