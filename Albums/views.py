import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as system_login, logout as system_logout, authenticate

from django.contrib.auth.models import User

from django.views.decorators.http import require_POST, require_GET

from rest_framework.decorators import api_view
from rest_framework.response import Response

from Albums.serializers import *

from Albums.models import *


# Create your views here.
@api_view(["GET"])
def getPics(request):
    pics = Albums.objects.all()
    serializer = TaskSerializer(pics,many=True)
    return Response(serializer.data)


def BodyLoader(body):
    try:
        return json.loads(body)
    except Exception:
        return {}

@require_POST
def signUp(request):
    if request.user.is_authenticated:
        system_logout(request)
    data = {}

    if request.POST:
        data = request.POST
    elif request.body:
        data = BodyLoader(request.body)
    
    
    username = data.get("username")
    password = data.get("password")
    print(username,password)

    try:
        user = User.objects.create_user(username,None,password)
        system_login(request,user)
        
        return JsonResponse({
            "status": "success"
        })
    except Exception as exept:
        print(exept)

        return JsonResponse({
            "status": "failed"
        })
