from django.db import models

# Create your models here.


class User(models.Model):
    # 用户账号、要唯一
    userAccount = models.CharField(max_length=20, unique=True)
    # 密码
    userPasswd = models.CharField(max_length=20)
    # 昵称
    userName = models.CharField(max_length=20)
    # 手机号
    userPhone = models.CharField(max_length=20)
    # 地址
    userAdderss = models.CharField(max_length=100)
    # 头像路径
    userImg = models.CharField(max_length=150)
    # 等级
    userRank = models.IntegerField()
    # touken 验证值，每次登陆后都会更新
    userToken = models.CharField(max_length=50)


    @classmethod
    def createuser(cls, account, passwd, name, phone, address, img, rank, token):
        u = cls(userAccount = account, userPasswd = passwd, userName = name, userPhone = phone, userAdderss = address, \
                userImg=img, userRank=rank, userToken=token)
        return u


class EyeDetect(models.Model):
    # 具体视频时间
    userTime = models.CharField(max_length=40, unique=False)
    # ear
    userEar = models.FloatField(max_length=40)
    # 状态
    userStatus = models.IntegerField()
    # 创建时间
    userCreateTime = models.CharField(max_length=40)
    # 用户昵称
    userNickName = models.CharField(max_length=40, default='unknown')
    # 检测类型
    userDetectClass = models.CharField(max_length=40, default='unknown')


class FacePose(models.Model):
    # 具体视频时间
    userTime = models.CharField(max_length=40, unique=False)
    # pitch
    userPitch = models.FloatField(max_length=40)
    # 状态
    userStatus = models.IntegerField()
    # 创建时间
    userCreateTime = models.CharField(max_length=40)
    # 用户昵称
    userNickName = models.CharField(max_length=40, default='unknown')
    # 检测类型
    userDetectClass = models.CharField(max_length=40, default='unknown')

class GazeTrack(models.Model):
    # 具体视频时间
    userTime = models.CharField(max_length=40, unique=False)
    # gaze
    userGaze = models.FloatField(max_length=40)
    # 状态
    userStatus = models.IntegerField()
    # 创建时间
    userCreateTime = models.CharField(max_length=40)
    # 用户昵称
    userNickName = models.CharField(max_length=40, default='unknown')
    # 检测类型
    userDetectClass = models.CharField(max_length=40, default='unknown')