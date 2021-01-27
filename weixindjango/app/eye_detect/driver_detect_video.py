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


def init_detecting(video_path):
    print('请勿眨眼，平视镜头，持续10秒。')
    # 初始化DLIB的人脸检测器（HOG），然后创建面部标志物预测
    print("[INFO] loading facial landmark predictor...")
    # 第一步：使用dlib.get_frontal_face_detector() 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # 第二步：使用dlib.shape_predictor获得脸部特征位置检测器
    predictor = dlib.shape_predictor('./app/eye_detect/model/shape_predictor_68_face_landmarks.dat')

    # 第三步：分别获取左右眼面部标志的索引
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # 第四步：打开cv2 本地摄像头
    cap = cv2.VideoCapture(video_path)
    list_ear = []
    TIME_10 = time.time()
    ear = 0
    # 从视频流循环帧
    while True:
        # 第五步：进行循环，读取图片，并对图片做维度扩大，并进灰度化
        start = time.time()
        ret, frame = cap.read()
        if ((time.time() - TIME_10) > 10) | (frame is None):
            print('视频检测采样结束')
            break
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
        if ear == 0:
            print('未检测到人脸')
        else:
            print('眼睛实时长宽比:{:.2f} '.format(ear))
        T = time.time() - start
        fps = 1 / T  # 实时在视频上显示fps
        print("实时fps：" + str(fps))

        # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放摄像头 release camera
    cap.release()
    return list_ear


def initial_train(list_ear):
    SAMPLE_RATE = 0.075
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
        for j in range(len(find_list[i])):
            if find_list[i][j] < 6 | find_list[i][j] > (len(list_ear) - 6 - 1):
                continue
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
                                                                                              train_size=0.99,
                                                                                              test_size=0.01)
    # 3.训练svm分类器
    classifier = svm.SVC(C=2, kernel='rbf', gamma=10, decision_function_shape='ovo')  # ovo:一对一策略
    classifier.fit(train_data, train_label)  # ravel函数在降维时默认是行序优先

    joblib.dump(classifier, './app/eye_detect/model/driver_svm.pkl')


def driver_detecting_video(VideoName):
    video_path = './app/eye_detect/uploadvideo/' + VideoName
    list_ear = init_detecting(video_path)
    initial_train(list_ear)

    ALLEAR=[]
    ALLTIME=[]
    ALLSTATUS=[]
    DOZING_FLAG = 0
    EYE_AR_CONSEC_FRAMES = 5
    EYE_CLOSING_FRAMES = 5  # 打瞌睡
    # 初始化帧计数器和眨眼总数
    COUNTER = 0
    TOTAL = 0

    # 初始化svm分类器
    classifier = joblib.load('./app/eye_detect/model/driver_svm.pkl')

    # 初始化DLIB的人脸检测器（HOG），然后创建面部标志物预测
    print("[INFO] loading facial landmark predictor...")
    # 第一步：使用dlib.get_frontal_face_detector() 获得脸部位置检测器
    detector = dlib.get_frontal_face_detector()
    # 第二步：使用dlib.shape_predictor获得脸部特征位置检测器
    predictor = dlib.shape_predictor('./app/eye_detect/model/shape_predictor_68_face_landmarks.dat')

    # 第三步：分别获取左右眼面部标志的索引
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # 第四步：打开cv2 本地摄像头
    cap = cv2.VideoCapture(video_path)

    # 视频的宽度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 视频的高度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 视频的编码
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    # 定义视频输出
    oVideoWriter = cv2.VideoWriter("./app/static/video/"+VideoName, fourcc, fps, (width, height))

    list_ear = []
    numframe = 0
    numframe3 = []
    BLINK_TIME=0
    SLEEP_TIME=0
    # 从视频流循环帧
    while True:
        # 第五步：进行循环，读取图片，并对图片做维度扩大，并进灰度化
        ear = 0
        DOZING_FLAG = 0
        start = time.time()
        ret, frame = cap.read()
        if frame is None:
            print('视频检测结束')
            break
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
            print('眼睛实时长宽比:{:.2f} '.format(ear))

            if ear == 0:
                print('未检测到眼睛')
                list_ear.clear()
                continue;

            list_ear.append(ear)
            if len(list_ear) == 13:
                list_label = classifier.predict([list_ear])  # 测试集的预测标签
                '''
                    分别计算左眼和右眼的评分求平均作为最终的评分，如果小于阈值，则加1，如果连续3次都小于阈值，则表示进行了一次眨眼活动
                '''
                # 第十三步：循环，满足条件的，眨眼次数+1
                if list_label[0] == 1:
                    COUNTER += 1
                    print(COUNTER)
                    # 如果连续5次都小于阈值，则表示进行了一次眨眼活动
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:  # 阈值：5
                        TOTAL += 1
                        numframe3.append(numframe)
                        print(',此处眨眼，时间：' + str(numframe / 30) + 's')
                        DOZING_FLAG = 1
                        BLINK_TIME=BLINK_TIME+1
                        # 重置眼帧计数器
                        COUNTER = 0
                        if TOTAL >= EYE_CLOSING_FRAMES:
                            if (numframe3[EYE_AR_CONSEC_FRAMES - 1] - numframe3[0]) < 50:
                                print(',此处打瞌睡，时间：' + str(numframe / 30) + 's')
                                DOZING_FLAG = 2
                                SLEEP_TIME=SLEEP_TIME+1
                                TOTAL=0
                        if len(numframe3)==6:
                            numframe3.pop(0)

                else:
                    COUNTER = 0
                    print(COUNTER)

                # ALLEAR_TIME_STATUS 该列表1为ear向量，2为时间，3为眼睛状态
                ALLEAR.append(ear)
                ALLTIME.append(numframe / cv2.CAP_PROP_FPS)
                ALLSTATUS.append(DOZING_FLAG)

                list_ear.pop(0)

                # 第十一步：使用cv2.convexHull获得凸包位置，使用drawContours画出轮廓位置进行画图操作
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # 第十二步：进行画图操作，用矩形框标注人脸
                left = rect.left()
                top = rect.top()
                right = rect.right()
                bottom = rect.bottom()
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

                # 第十四步：进行画图操作，68个特征点标识
                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                # 第十五步：进行画图操作，同时使用cv2.putText将眨眼次数进行显示
                cv2.putText(frame, "Faces: {}".format(len(rects)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "Blinks: {}".format(BLINK_TIME), (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "Sleeps: {}".format(SLEEP_TIME), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if DOZING_FLAG == 0:
                    cv2.putText(frame, "NORMAL", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                elif DOZING_FLAG == 1:
                    cv2.putText(frame, "BLINK!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                elif DOZING_FLAG == 2:
                    cv2.putText(frame, "SLEEP!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        T = time.time() - start
        fps = 1 / T  # 实时在视频上显示fps
        fps_txt = 'fps:%.2f' % (fps)
        cv2.putText(frame, fps_txt, (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, 8)
        # 窗口显示 show with opencv
        # cv2.imshow("Frame", frame)
        frame = imutils.resize(frame, width=width)
        oVideoWriter.write(frame)

        # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头 release camera
    cap.release()
    oVideoWriter.release()
    # do a bit of cleanup
    cv2.destroyAllWindows()
    ALLEAR_TIME_STATUS=[ALLEAR,ALLTIME,ALLSTATUS]
    return ALLEAR_TIME_STATUS
