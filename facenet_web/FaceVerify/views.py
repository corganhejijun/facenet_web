from django.shortcuts import render
from django.http import JsonResponse
import os
# from . import compare

FACE_SAMPLE = "FaceVerify\\face"

def index(request):
    fileList = []
    baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE, "sample")
    for file in os.listdir(baseDir):
        if file.endswith(".jpg"):
            fileList.append(os.path.join(FACE_SAMPLE, "sample", file))
    return render(request, 'FaceVerify/index.html', {'faceList':fileList})

def json(request):
    func = request.GET['func']
    if func == 'compare':
        data1 = request.GET['data1']
        data2 = request.GET['data2']
        baseDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", FACE_SAMPLE)
        path1 = os.path.join(baseDir, data1)
        path2 = os.path.join(baseDir, data2)
        result = compare.compare([path1, path2])
        return JsonResponse({'flag':True,'result':result})
    return JsonResponse({'flag':False})