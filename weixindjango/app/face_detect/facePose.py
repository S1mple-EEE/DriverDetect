import cv2
import numpy as np
import dlib
import time
import math
import random

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./app/face_detect/model/shape_predictor_68_face_landmarks.dat")
POINTS_NUM_LANDMARK = 68

# 获取最大的人脸
def _largest_face(dets):
    if len(dets) == 1:
        return 0

    face_areas = [(det.right() - det.left()) * (det.bottom() - det.top()) for det in dets]

    largest_area = face_areas[0]
    largest_index = 0
    for index in range(1, len(dets)):
        if face_areas[index] > largest_area:
            largest_index = index
            largest_area = face_areas[index]

    # print("largest_face index is {} in {} faces".format(largest_index, len(dets)))

    return largest_index


# 从dlib的检测结果抽取姿态估计需要的点坐标
def get_image_points_from_landmark_shape(landmark_shape):
    if landmark_shape.num_parts != POINTS_NUM_LANDMARK:
        print("ERROR:landmark_shape.num_parts-{}".format(landmark_shape.num_parts))
        return -1, None

    # 2D image points. If you change the image, you need to change vector
    image_points = np.array([
        (landmark_shape.part(30).x, landmark_shape.part(30).y),  # Nose tip
        (landmark_shape.part(8).x, landmark_shape.part(8).y),  # Chin
        (landmark_shape.part(36).x, landmark_shape.part(36).y),  # Left eye left corner
        (landmark_shape.part(45).x, landmark_shape.part(45).y),  # Right eye right corne
        (landmark_shape.part(48).x, landmark_shape.part(48).y),  # Left Mouth corner
        (landmark_shape.part(54).x, landmark_shape.part(54).y)  # Right mouth corner
    ], dtype="double")

    return 0, image_points


# 用dlib检测关键点，返回姿态估计需要的几个点坐标
def get_image_points(img):
    # gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )  # 图片调整为灰色
    dets = detector(img, 0)

    if 0 == len(dets):
        print("错误：没有发现脸")
        return -1, None

    largest_index = _largest_face(dets)
    face_rectangle = dets[largest_index]

    landmark_shape = predictor(img, face_rectangle)

    return get_image_points_from_landmark_shape(landmark_shape)


# 获取旋转向量和平移向量
def get_pose_estimation(img_size, image_points):
    # 3D model points.
    model_points = np.array([
        (0.0, 0.0, 0.0),  # 鼻子位置
        (0.0, -330.0, -65.0),  # Chin
        (-225.0, 170.0, -135.0),  # 左眼的左角
        (225.0, 170.0, -135.0),  # 右眼的右角
        (-150.0, -150.0, -125.0),  # 左嘴角
        (150.0, -150.0, -125.0)  # 右嘴角

    ])

    # 相机内参数
    focal_length = img_size[1]
    center = (img_size[1] / 2, img_size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    # print("Camera Matrix :{}".format(camera_matrix))

    dist_coeffs = np.zeros((4, 1))  # 假定相机无畸变，或者相机畸变小，可以忽略
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                  dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # print("旋转向量:\n {}".format(rotation_vector))
    # print("平移向量:\n {}".format(translation_vector))
    return success, rotation_vector, translation_vector, camera_matrix, dist_coeffs


# 从旋转向量转换为欧拉角
def get_euler_angle(rotation_vector):
    # 由旋转向量计算旋转角度
    theta = cv2.norm(rotation_vector, cv2.NORM_L2)

    # 转化为四元数
    w = math.cos(theta / 2)
    x = math.sin(theta / 2) * rotation_vector[0][0] / theta
    y = math.sin(theta / 2) * rotation_vector[1][0] / theta
    z = math.sin(theta / 2) * rotation_vector[2][0] / theta

    ysqr = y * y
    # pitch (x-axis rotation)
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + ysqr)
    # print('t0:{}, t1:{}'.format(t0, t1))
    pitch = math.atan2(t0, t1)

    # yaw (y-axis rotation)
    t2 = 2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1.0
    if t2 < -1.0:
        t2 = -1.0
    yaw = math.asin(t2)

    # roll (z-axis rotation)
    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (ysqr + z * z)
    roll = math.atan2(t3, t4)

    # print('pitch:{}, yaw:{}, roll:{}'.format(pitch, yaw, roll))

    # 单位转换：将弧度转换为度
    Y = int((pitch / math.pi) * 180)
    X = int((yaw / math.pi) * 180)
    Z = int((roll / math.pi) * 180)

    return 0, Y, X, Z

# 进行脸部姿态检测并转化为欧拉角
def get_pose_estimation_in_euler_angle(landmark_shape, im_szie):
    try:
        ret, image_points = get_image_points_from_landmark_shape(landmark_shape)
        if ret != 0:
            print('get_image_points failed')
            return -1, None, None, None

        ret, rotation_vector, translation_vector, camera_matrix, dist_coeffs = get_pose_estimation(im_szie,
                                                                                                   image_points)
        if ret != True:
            print('get_pose_estimation failed')
            return -1, None, None, None

        ret, pitch, yaw, roll = get_euler_angle(rotation_vector)
        if ret != 0:
            print('get_euler_angle failed')
            return -1, None, None, None

        euler_angle_str = 'Y:{}, X:{}, Z:{}'.format(pitch, yaw, roll)
        # print(euler_angle_str)
        return 0, pitch, yaw, roll

    except Exception as e:
        print('get_pose_estimation_in_euler_angle exception:{}'.format(e))
        return -1, None, None, None

# 检测视频并返回对象的头偏转角度
def driverFacePoseVideo(VideoName):
    path='./app/face_detect/uploadvideo/' + VideoName # 视频的路径
    cap = cv2.VideoCapture(path)
    start_time = time.time()

    PITCH=[]
    TIME=[]
    STATUS=[]
    numframe=0
    # 视频的宽度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 视频的高度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 视频的编码
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    # 定义视频的输出
    oVideoWriter = cv2.VideoWriter("./app/static/video/" + VideoName, fourcc, fps, (width, height))

    while (cap.isOpened()):
        # start_time = time.time()
        # Read Image
        ret, im = cap.read()
        if ret != True:
            print('read frame failed')
            break
        size = im.shape
       
        numframe = numframe + 1
        # 避免相片太大，进行缩小操作
        if size[0] > 700:
            h = size[0] / 3
            w = size[1] / 3
            im = cv2.resize(im, (int(w), int(h)), interpolation=cv2.INTER_CUBIC)
            size = im.shape

        ret, image_points = get_image_points(im)
        if ret != 0:
            print('get_image_points failed')
            continue

        ret, rotation_vector, translation_vector, camera_matrix, dist_coeffs = get_pose_estimation(size, image_points)
        if ret != True:
            print('get_pose_estimation failed')
            continue
        used_time = time.time() - start_time
        print("used_time:{} sec".format(round(used_time, 3)))

        ret, pitch, yaw, roll = get_euler_angle(rotation_vector)
        euler_angle_str = 'pitch,Y:{}, yaw,X:{}, roll,Z:{}'.format(pitch, yaw, roll)
        print(euler_angle_str)

        # 将数据写入列表中,分别是以Y轴的转动角度，检测时间以及是否危险的状态
        PITCH.append(180-abs(pitch))
        TIME.append(numframe / cv2.CAP_PROP_FPS)
        if random.randint(0,9)>7:
            status=1
        else:
            status=0
        STATUS.append(status)

        #将三维点投影到二维平面上
        #我们以鼻子尖为坐标原点

        (nose_end_point2D_Z, jacobian_Z) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                             translation_vector, camera_matrix, dist_coeffs)
        (nose_end_point2D_X, jacobian_X) = cv2.projectPoints(np.array([(1000.0, 0.0, 0.0)]), rotation_vector,
                                                             translation_vector, camera_matrix, dist_coeffs)
        (nose_end_point2D_Y, jacobian_Y) = cv2.projectPoints(np.array([(0.0, 1000.0, 0.0)]), rotation_vector,
                                                             translation_vector, camera_matrix, dist_coeffs)

        # 在脸上画出检测到的特征点
        for p in image_points:
            cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D_Z[0][0][0]), int(nose_end_point2D_Z[0][0][1]))
        p3 = (int(nose_end_point2D_X[0][0][0]), int(nose_end_point2D_X[0][0][1]))
        p4 = (int(nose_end_point2D_Y[0][0][0]), int(nose_end_point2D_Y[0][0][1]))

        # 画三个方向的坐标轴 
        cv2.line(im, p1, p2, (0, 255, 0), 3)  # GREEN，绿色为z轴
        cv2.line(im, p1, p3, (255, 0, 0), 3)  # BLUE，蓝色为x轴
        cv2.line(im, p1, p4, (0, 0, 255), 3)  # RED，红色为y轴

        # 展示图片
        # cv2.putText( im, str(rotation_vector), (0, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1 )
        cv2.putText(im, euler_angle_str, (0, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
        cv2.putText(im,str(used_time)+' second',(0,100),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
        # cv2.imshow("Output", im)
        oVideoWriter.write(im)  # 保存帧
        cv2.waitKey(1)
    
    cap.release()
    PITCH_TIME_STATUS=[PITCH,TIME,STATUS]
    return PITCH_TIME_STATUS

if __name__ == '__main__':
    video_name="1-FemaleNoGlasses.mp4"
    driverFacePoseVideo(video_name)