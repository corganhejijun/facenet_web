from django.shortcuts import render
from django.http import JsonResponse
import os

# from . import compare
from .models import User
from django.contrib.auth.hashers import make_password

FACE_SAMPLE = "FaceVerify\\face"

def index(request):
    fileList = []
    user = ""
    baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE, "sample")
    for file in os.listdir(baseDir):
        if file.endswith(".jpg"):
            fileList.append(os.path.join(FACE_SAMPLE, "sample", file))
    return render(request, 'FaceVerify/index.html', {'faceList':fileList, "user": user})

def json(request):
    func = request.GET['func']
    if func == 'compare':
        data1 = request.GET['data1']
        data2 = request.GET['data2']
        baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE)
        path1 = os.path.join(baseDir, data1)
        path2 = os.path.join(baseDir, data2)
        result = compare.compare([path1, path2])
    elif func == 'register':
        return register(request.GET['username'], request.GET['password'])
    elif func == 'login':
        return loginProcess(request.GET['username'], request.GET['password'])
    return JsonResponse({'flag':False})

def register(username, password):
    result = False
    user = User(username=username, password=make_password(password))
    user.save()
    result = True
    return JsonResponse({'flag':result})

def loginProcess(username, password):
    result = False
    User.objects.get(username=username, password=make_password(password))
    return JsonResponse({'flag':result})

def login(request):
    return render(request, 'FaceVerify/login.html');