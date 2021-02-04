from app.models import User,EyeDetect
from django.http import HttpResponse
import base64
import numpy as np
import uuid
import cv2
import os
import json
import glob
import time
import json
from app.eye_detect.eye_detect_frame import eye_detect_frame
from app.eye_detect.driver_detect_frame import driver_detecting_frame
from app.eye_detect.driver_detect_video import driver_detecting_video


from django.conf import settings
BASE_DIR = settings.BASE_DIR


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        try:
            user = User.objects.get(userAccount=username)
            if user.userPasswd != passwd:
                return HttpResponse("用户名或密码错误")

        except User.DoesNotExist as e:
            return HttpResponse("用户名不存在")
        # 登录成功
        print(username)
        print(passwd)
        return HttpResponse("登录成功！")
    else:
        return HttpResponse("请求错误")

def initialload(request):
    if request.method == "POST":
        imgdicBase64 = request.POST.dict()
        imgarrBase64 = list(imgdicBase64.values())
        for imgBase64 in imgarrBase64:
            img = base64.b64decode(imgBase64)
            nparr = np.fromstring(img, np.uint8)
            nparr=nparr.reshape((640,480,4))
            imgnp=nparr[:,:,[2,1,0]]
            imgid=uuid.uuid1()
            imgid='./app/tempimg/'+str(time.time())+'.jpg'
            cv2.imwrite(imgid,imgnp)
        path_file_number = glob.glob(pathname='./app/tempimg/*.jpg')  # 获取当前文件夹下个数
        print(len(path_file_number))
        result = {"imgNum": len(path_file_number)}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type = "application/json,charset=utf-8")
    else:
        return HttpResponse("请求错误")

def initialtrain(request):
    if request.method == "POST":
        path = './app/tempimg/'
        imgdirlist = os.listdir(path)
        DOZING_FLAG=eye_detect_frame(imgdirlist)
        result = {"status": DOZING_FLAG,"info":"预训练完成"}
        return HttpResponse(result)
    else:
        return HttpResponse("请求错误")


def driverdetect(request):
    if request.method == "POST":
        video_path = './app/eye_detect/images/1-FemaleNoGlasses.avi'
        DOZING_FLAG = driver_detecting_frame(video_path)
        result = {"status": DOZING_FLAG, "info": "预训练完成"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type = "application/json,charset=utf-8")
    else:
        return HttpResponse("请求错误")


def cleartempimg(request):
    path = './app/tempimg'
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            for f in os.listdir(path_file):
                path_file2 = os.path.join(path_file, f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)
    return HttpResponse("文件夹已清空")

def getVideo(request):
    if request.method == 'POST':
        if request.FILES:
            myFile = request.FILES['file']
            dir = os.path.join(os.path.join(BASE_DIR, 'app\\eye_detect'),'uploadvideo')
            destination = open(os.path.join(dir, myFile.name),
                               'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            ALLEAR_TIME_STATUS= driver_detecting_video(myFile.name)
            # ALLEAR_TIME_STATUS=[[1,2,3],[1,2,3],[1,2,3]]
            videopath = "http://127.0.0.1:8000/app/static/video/" + myFile.name
            createtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            result = {"ear":ALLEAR_TIME_STATUS[0],"time":ALLEAR_TIME_STATUS[1],"status": ALLEAR_TIME_STATUS[2],"createtime":createtime}
            EyeInsertDB(ALLEAR_TIME_STATUS,createtime)

            jsondate = time.strftime("%a_%b_%d_%H.%M.%S_%Y", time.localtime())
            jsonfilename = "./app/static/json/eyedetect_"+jsondate+".json"
            with open(jsonfilename, 'w') as file_obj:
                json.dump(result, file_obj)

            ResponseResult = {"inserttime": createtime,"videopath":videopath,"category":"eye_detect"}
            return HttpResponse(json.dumps(ResponseResult, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('上传数据为空')
    else:
        return HttpResponse('请求错误')


def EyeInsertDB(ALLEAR_TIME_STATUS,tabdate):
    eyedetect_list = []
    for i in range(len(ALLEAR_TIME_STATUS[0])):
        eyedetect_list.append(EyeDetect(userTime=ALLEAR_TIME_STATUS[0][i],userEar=ALLEAR_TIME_STATUS[1][i],userStatus=ALLEAR_TIME_STATUS[2][i], userCreateTime=tabdate))
    EyeDetect.objects.bulk_create(eyedetect_list)
