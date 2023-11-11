from django.shortcuts import render
from .models import music_collection
from django.http import HttpResponse, JsonResponse
import json
from pymongo import MongoClient
from bson.json_util import dumps


# Create your views here.

def search_by_id(request):
    to_music_id = request.GET.get('id', '')

    if not to_music_id:
        return HttpResponse("No id provided")
    else:
        to_music_id = request.GET.get('id', '')  # /api/music_detail?id=[music_id]
        result = music_collection.find({"music_detail.music_id": int(to_music_id)},{"_id":0})
        print(list(result))
        print(type(result))
        return HttpResponse("search by id is finished")

def search_by_tag(request):
    to_music_tag = request.GET.get('tag','')

    if not to_music_tag:
        return HttpResponse("No tag provided")
    else:
        result = music_collection.find({"music_detail.music_type":str(to_music_tag)},
                                       {"music_detail.music_id":1, "music_detail.music_name":1, "singer_detail.singer_name":1 })
        print(list(result))
        print(type(result))
        return HttpResponse("search by tag is finished")

