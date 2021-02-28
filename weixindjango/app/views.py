from app.models import User,EyeDetect,FacePose
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
from app.face_detect.facePose import driverFacePoseVideo


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

#将EAR写入数据库
def EyeInsertDB(ALLEAR_TIME_STATUS,tabdate):
    eyedetect_list = []
    for i in range(len(ALLEAR_TIME_STATUS[0])):
        eyedetect_list.append(EyeDetect(userTime=ALLEAR_TIME_STATUS[0][i],userEar=ALLEAR_TIME_STATUS[1][i],userStatus=ALLEAR_TIME_STATUS[2][i], userCreateTime=tabdate))
    EyeDetect.objects.bulk_create(eyedetect_list)

def getVideo(request):
    if request.method == 'POST':
        if request.FILES:
            myFile = request.FILES['file']
            dir = os.path.join(os.path.join(BASE_DIR, 'app\\eye_detect'), 'uploadvideo')
            destination = open(os.path.join(dir, myFile.name),
                               'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            ALLEAR_TIME_STATUS = driver_detecting_video(myFile.name)
            # ALLEAR_TIME_STATUS = [[1, 2, 2], [1, 2, 3], [1, 2, 2]]

            videopath = "http://127.0.0.1:8000/app/static/video/" + myFile.name

            createtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            EyeInsertDB(ALLEAR_TIME_STATUS, createtime)

            ResponseResult = {"ear": ALLEAR_TIME_STATUS[0], "time": ALLEAR_TIME_STATUS[1],
                              "status": ALLEAR_TIME_STATUS[2], "createtime": createtime, "videopath": videopath,
                              "category": "eye_detect"}

            return HttpResponse(json.dumps(ResponseResult, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('上传数据为空')
    else:
        return HttpResponse('请求错误')


# 将Face数据写入数据库
def facePoseInsertDB(PITCH_TIME_STATUS,tabdate):
    facedetect_list=[]
    for i in range(len(PITCH_TIME_STATUS[0])):
        facedetect_list.append(FacePose(userTime=PITCH_TIME_STATUS[1][i],userPitch=PITCH_TIME_STATUS[0][i],userStatus=PITCH_TIME_STATUS[2][i], userCreateTime=tabdate))
    FacePose.objects.bulk_create(facedetect_list)

# 得到面部方向检测的视频
def getFaceVideo(request):
    if request.method == 'POST':
        # 将用户上传的视频文件写入到eyedetect\uploadvideo\文件夹下
        if request.FILES:
            myFile = request.FILES['file']
            dir = os.path.join(os.path.join(BASE_DIR, 'app\\face_detect'), 'uploadvideo')
            destination = open(os.path.join(dir, myFile.name),
                               'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            # 读取用户上传的video，并进行头部姿态检测，并将检测的结果保存到static/video/文件夹下
            PITCH_TIME_STATUS=driverFacePoseVideo(myFile.name)

            # 获取保存的头部姿态检测视频文件地址
            videopath = "http://127.0.0.1:8000/app/static/video/" + myFile.name

            createtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            facePoseInsertDB(PITCH_TIME_STATUS, createtime)

            # 创建时间
            createtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())

            # 返回给result.js 中option的数据通信值，包括结果视频的绝对地址、创建时间、检测类别等信息
            ResponseResult = {"createtime": createtime, "videopath": videopath, "category": "face_pose_detect"}
            return HttpResponse(json.dumps(ResponseResult, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('上传数据为空')
    else:
        return HttpResponse('请求错误')





