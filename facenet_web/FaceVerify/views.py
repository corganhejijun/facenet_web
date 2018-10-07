from django.shortcuts import render
from django.http import JsonResponse
import os

from . import compare
from .models import User, CompareResult
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from django.views.decorators.csrf import csrf_exempt

FACE_SAMPLE = "FaceVerify\\face"

def index(request):
    fileList = []
    user = ""
    if 'user' in request.session:
        user = request.session['user']
        userDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE, user)
        for file in os.listdir(userDir):
            fileList.append(os.path.join(FACE_SAMPLE, user, file))
    baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE, "sample")
    for file in os.listdir(baseDir):
        if file.endswith(".jpg"):
            fileList.append(os.path.join(FACE_SAMPLE, "sample", file))
    return render(request, 'FaceVerify/index.html', {'faceList':fileList, "user": user})

def getSim(distance):
    if distance < 0:
        return (-1 + distance) / 1.1
    return (1.1 - distance) / 1.1

def json(request):
    func = request.GET['func']
    if func == 'compare':
        data1 = request.GET['data1']
        data2 = request.GET['data2']
        if (data1 == data2):
            return JsonResponse({'flag': True, 'result': 1})
        if data1 < data2:
            t = data2
            data2 = data1
            data1 = t
        compResult = CompareResult.objects.filter(img1=data1, img2=data2).first()
        if compResult:
            return JsonResponse({'flag': True, 'result': str(getSim(compResult.distance))})
        baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE)
        path1 = os.path.join(baseDir, data1)
        path2 = os.path.join(baseDir, data2)
        try:
            result = compare.compare([path1, path2])
            compResult = CompareResult(img1=data1, img2=data2, distance=result)
            compResult.save()
            return JsonResponse({'flag': True, 'result': str(getSim(result))})
        except Exception as err:
            return JsonResponse({'flag': False, 'result': str(err)})
    elif func == 'register':
        return register(request.GET['username'], request.GET['password'])
    elif func == 'login':
        return loginProcess(request, request.GET['username'], request.GET['password'])
    elif func == 'logout':
        del request.session['user']
        request.session.modified = True
    return JsonResponse({'flag':False})

def register(username, password):
    result = False
    user = User(username=username, password=make_password(password))
    user.save()
    result = True
    return JsonResponse({'flag':result})

def loginProcess(request, username, password):
    result = False
    try:
        user = User.objects.get(username=username)
        result = check_password(password, user.password)
        if result and 'user' not in request.session:
            request.session['user'] = username
            request.session.modified = True
    except:
        pass
    return JsonResponse({'flag':result})

def login(request):
    return render(request, 'FaceVerify/login.html');

@csrf_exempt
def upload(request):
    result = False
    if request.method != 'POST' or 'user' not in request.session:
        return JsonResponse({'flag':result})
    file = request.FILES.get('inputface')
    if file:
        saveDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE, request.session['user'])
        if not os.path.isdir(saveDir):
            os.mkdir(saveDir)
        with open(os.path.join(saveDir, file.name),'wb') as f:   #  新建1张图片 ，图片名称为 上传的文件名
            for temp in file.chunks():                #  往图片添加图片信息
                f.write(temp)
            result = True
    return JsonResponse({'flag':result})
        