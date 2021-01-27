# -*- coding: utf-8 -*-
# import the necessary packages
from scipy.spatial import distance as dist
from sklearn import svm
import sklearn
from sklearn.metrics import accuracy_score
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np  # 数据处理的库 numpy
import imutils
import time
import dlib
import cv2
import os
import heapq
from sklearn.externals import joblib

def eye_aspect_ratio(eye):
    # 垂直眼标志（X，Y）坐标
    A = dist.euclidean(eye[1], eye[5])  # 计算两个集合之间的欧式距离
    B = dist.euclidean(eye[2], eye[4])
    # 计算水平之间的欧几里得距离
    # 水平眼标志（X，Y）坐标
    C = dist.euclidean(eye[0], eye[3])
    # 眼睛长宽比的计算
    ear = (A + B) / (2.0 * C)
    # 返回眼睛的长宽比
    return ear


def init_detecting(imgdirlist):
    # 初始化DLIB的人脸检测器（HOG），然后创建面部标志物预测
    print("[INFO] loading facial landmark predictor...")
    # 第一步：使用dlib.get_frontal_face_detector() 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # 第二步：使用dlib.shape_predictor获得脸部特征位置检测器
    predictor = dlib.shape_predictor('./app/eye_detect/model/shape_predictor_68_face_landmarks.dat')

    # 第三步：分别获取左右眼面部标志的索引
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    list_ear = []
    ear=0
    # 从视频流循环帧
    for i in imgdirlist:
        # 第五步：进行循环，读取图片，并对图片做维度扩大，并进灰度化
        i="app/tempimg/"+i
        frame = cv2.imread(i)

        frame = imutils.resize(frame, width=720)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 第六步：使用detector(gray, 0) 进行脸部位置检测
        rects = detector(gray, 0)

        # 第七步：循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
        for rect in rects:
            shape = predictor(gray, rect)

            # 第八步：将脸部特征信息转换为数组array的格式
            shape = face_utils.shape_to_np(shape)

            # 第九步：提取左眼和右眼坐标
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            # 第十步：构造函数计算左右眼的EAR值，使用平均值作为最终的EAR
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            list_ear.append(ear)
    return list_ear

def initial_train(list_ear):
    SAMPLE_RATE = 0.1
    topk = int(SAMPLE_RATE * len(list_ear))
    min_idx = map(list_ear.index, heapq.nsmallest(topk, list_ear))
    min_idx = list(map(int, min_idx))
    min_idx.sort()

    s = 1
    find_list = []
    have_list = []
    while s <= len(min_idx) - 1:
        if min_idx[s] - min_idx[s - 1] == 1:
            flag = s - 1
            while (min_idx[s] - min_idx[s - 1] == 1):
                s += 1
                if (s == len(min_idx)):
                    break
            find_list.append(min_idx[flag:s])
            have_list += min_idx[flag:s]
        else:
            s += 1

    min_idx = []
    alllist_min = []
    other_idx = []
    alllist_other = []
    identity_min = []
    identity_other = []
    for i in range(len(find_list)):
        if (find_list[i][-1] < 6):
            continue
        for j in range(len(find_list[i])):
            min_idx.append(find_list[i][j])
            identity_min.append(1)
            alllist_min.append(list_ear[(find_list[i][j] - 6):(find_list[i][j] + 6 + 1)])

    for i in range(6, (len(list_ear) - 6)):
        inter = list(set(range((i - 6), (i + 6 + 1))).intersection(set(min_idx)))
        if len(inter) == 0:
            alllist_other.append(list_ear[(i - 6):(i + 6 + 1)])
            identity_other.append(0)
        else:
            continue

    x = alllist_min + alllist_other
    y = identity_min + identity_other

    # 2.划分数据与标签
    train_data, test_data, train_label, test_label = sklearn.model_selection.train_test_split(x, y, random_state=1,
                                                                                              train_size=0.9,
                                                                                              test_size=0.1)
    # 3.训练svm分类器
    classifier = svm.SVC(C=2, kernel='rbf', gamma=10, decision_function_shape='ovo')  # ovo:一对一策略
    classifier.fit(train_data, train_label)  # ravel函数在降维时默认是行序优先

    joblib.dump(classifier,'./app/eye_detect/model/svm.pkl')

def eye_detect_frame(imgdirlist):
    list_ear=init_detecting(imgdirlist)
    initial_train(list_ear)

    alllist_ear = []
    DOZING_FLAG=0

    # 定义两个常数
    EYE_AR_CONSEC_FRAMES = 2#眨眼
    EYE_CLOSING_FRAMES = 5#打瞌睡

    # 初始化帧计数器和眨眼总数
    COUNTER = 0
    TOTAL = 0

    # 初始化svm分类器
    classifier = joblib.load('./app/eye_detect/model/svm.pkl')

    # 初始化DLIB的人脸检测器（HOG），然后创建面部标志物预测
    print("[INFO] loading facial landmark predictor...")
    # 第一步：使用dlib.get_frontal_face_detector() 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # 第二步：使用dlib.shape_predictor获得脸部特征位置检测器
    predictor = dlib.shape_predictor('app/eye_detect/model/shape_predictor_68_face_landmarks.dat')

    # 第三步：分别获取左右眼面部标志的索引
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    list_ear = []
    numframe = 0
    numframe3 = []

    # 从视频流循环帧
    for i in imgdirlist:
        start = time.time()
        # 第五步：进行循环，读取图片，并对图片做维度扩大，并进灰度化
        ear = 0
        i = "../tempimg/" + i
        frame = cv2.imread(i)
        numframe = numframe + 1
        frame = imutils.resize(frame, width=720)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 第六步：使用detector(gray, 0) 进行脸部位置检测
        rects = detector(gray, 0)

        # 第七步：循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
        for rect in rects:
            shape = predictor(gray, rect)

            # 第八步：将脸部特征信息转换为数组array的格式
            shape = face_utils.shape_to_np(shape)

            # 第九步：提取左眼和右眼坐标
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            # 第十步：构造函数计算左右眼的EAR值，使用平均值作为最终的EAR
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            list_ear.append(ear)
            if len(list_ear) == 13:
                alllist_ear.append(list_ear)
                list_label = classifier.predict([list_ear])  # 测试集的预测标签

                '''
                    分别计算左眼和右眼的评分求平均作为最终的评分，如果小于阈值，则加1，如果连续3次都小于阈值，则表示进行了一次眨眼活动
                '''
                # 第十三步：循环，满足条件的，眨眼次数+1

                if list_label == 1:
                    COUNTER += 1
                    print(COUNTER)
                    # 如果连续5次都小于阈值，则表示进行了一次眨眼活动
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:  # 阈值：5
                        TOTAL += 1
                        numframe3.append(numframe)
                        print(',此处眨眼，时间：' + str(numframe / 30) + 's')
                        DOZING_FLAG=1
                        # 重置眼帧计数器
                        COUNTER = 0
                        if (TOTAL >= EYE_CLOSING_FRAMES):
                            if ((numframe3[5] - numframe3[0]) < 50):
                                print(',此处打瞌睡，时间：' + str(numframe / 30) + 's')
                                DOZING_FLAG=2
                            numframe3.pop(0)
                else:
                    COUNTER = 0
                    print(COUNTER)
                list_ear.pop(0)
            if ear == 0:
                print('未检测到人脸')
            else:
                print('眼睛实时长宽比:{:.6f} '.format(ear))
        T = time.time() - start
        fps = 1 / T  # 实时在视频上显示fps
        print('实时fps:'+str(fps))
    return DOZING_FLAG

if __name__ == '__main__':
    path = '../tempimg'
    imgdirlist = os.listdir(path)
    list_ear=init_detecting(imgdirlist)
    initial_train(list_ear)
    eye_detect(imgdirlist)

