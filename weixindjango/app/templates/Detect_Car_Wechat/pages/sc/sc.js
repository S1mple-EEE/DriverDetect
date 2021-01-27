// pages/sc/sc.js
var app=getApp();
Page({

  data: {
    result: "",                 // 结果文本
    resimg:"",                  //结果图片地址
    resulttop: "请上传车辆照片",
    img_url: "",                //上传图片地址
    isLoading: false,           //判断正在上传的中间变量
    result_status: 'none',
    picture: '../picture/shangchuanshipin.png',    //初始显示图片（可改）
    buttonLoad: "查看结果",

    // 以下数据含义同上，只用来显示四角照
    isLoading1: false,
    result_status1: 'none',
    img_url1: "",
    picture1: 'data:image/png;base64,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',

    isLoading2: false,
    result_status2: 'none',
    img_ur2: "",
    picture2: 'data:image/png;base64,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',

    isLoading3: false,
    result_status3: 'none',
    img_url3: "",
    picture3: 'data:image/png;base64,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',

    isLoading4: false,
    result_status4: 'none',
    img_url4: "",
    picture4: 'data:image/png;base64,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',

    clickFlag:true //防重复点击
  },

  // 上传图片函数
  upload: function(e) {
    console.log("upload")
    let that = this
    wx.chooseImage({
      success: function(res) {
        let tmpFile = res.tempFilePaths[0]
        that.setData({
          img_url: tmpFile
        })
        that.setData({
          isLoading: true
        })
        wx.showToast({
          title: '加载中...',
          mask: true,
          icon: 'loading',
          duration: 10000
        }),
        wx.uploadFile({
          url: 'https://lamaric.goho.co/upload/', //app.ai_api.File.file
          filePath: tmpFile, //文件路径  这里是img文件
          name: 'file', //与后端适配，一般别动
          formData: {
            method: 'POST' //请求方式
          },
          success(res) {
            if (res.statusCode == 200) {
              var data = JSON.parse(res.data);
              console.log('OK')
              wx.showToast({
                title: '上传成功！',
              })
              that.setData({
                isLoading: false
              })
              // let data = JSON.parse(data.result)
              console.log(data)
              // 以下赋值
              that.setData({
                result: data.result,
                resimg: data.combine_url
              })
              if (data.result===null){
                var by=[{"part":"未检测到","type":"--","price":0}]
                getApp().globalData.resultfinally = by,
                getApp().globalData.resultimg = data.combine_url
              }else{
                getApp().globalData.resultfinally = data.result,
                getApp().globalData.resultimg = data.combine_url
              }
              that.setData({
                result_status: 'inline'
              })
              that.tapToRes()
            } else {
              console.log('上传失败')
              wx.showToast({
                title: '上传失败！',
                icon: 'none'
              })
            }
          }
        })

      },
    })
  },

  // 选择图片显示函数（不上传，用于四角照）
  upload1: function(e) {
 console.log("chooseVideo")
    this.setData({clickFlag: false})
 
    let that = this
    //1.拍摄视频或从手机相册中选择视频
    wx.chooseVideo({
      sourceType: ['album', 'camera'], // album 从相册选视频，camera 使用相机拍摄
      // maxDuration: 60, // 拍摄视频最长拍摄时间，单位秒。最长支持60秒
      camera: 'back',//默认拉起的是前置或者后置摄像头，默认back
      compressed: true,//是否压缩所选择的视频文件
      success: function(res){
        console.log(res)
        let tempFilePath = res.tempFilePath//选择定视频的临时文件路径（本地路径）
        let duration = res.duration //选定视频的时间长度
        let size = parseFloat(res.size/1024/1024).toFixed(1) //选定视频的数据量大小
        // let height = res.height //返回选定视频的高度
        // let width = res.width //返回选中视频的宽度
        that.data.duration = duration
        if(parseFloat(size) > 100){
          that.setData({
            clickFlag: true,
            duration: ''
          })
          let beyondSize = parseFloat(size) - 100
          wx.showToast({
            title: '上传的视频大小超限，超出'+beyondSize+'MB,请重新上传',
            //image: '',//自定义图标的本地路径，image的优先级高于icon
            icon:'none'
          })
        }else{
          that.setData({
            img_url1: tempFilePath,
            isLoading1: true
          })
        }
      },
      fail: function() {
        // fail
      },
      complete: function() {
        // complete
      }
    })
  },

  eyedetect:function(e){
    let that = this
    wx.showLoading({
      title: '上传进度：0%',
      mask: true //是否显示透明蒙层，防止触摸穿透
    })
    const uploadTask = wx.uploadFile({
      url: 'http://127.0.0.1:8000/app/getVideo/',//开发者服务器地址
      filePath:that.data.img_url1,//要上传文件资源的路径（本地路径）
      name:'file',//文件对应key,开发者在服务端可以通过这个 key 获取文件的二进制内容
      // header: {}, // 设置请求的 header

      success: function(res){
        console.log("uploadFile",res)
        // success
        wx.hideLoading()
        if(res.statusCode == 200){
          let jsondata=JSON.parse(res.data)

          wx.navigateTo({
            url: '../result/result?jsondata='+encodeURIComponent(JSON.stringify(res.data)),
          })

          wx.showToast({
            title: '上传成功',
            icon: 'success'
          })
        }else{
          that.setData({
            videoUrl: '',
            poster: '',
            duration: '',
            clickFlag:true
          })
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          })
        }
       
      },
      fail: function() {
        // fail
        wx.hideLoading()
        this.setData({
          videoUrl: '',
          poster: '',
          duration: '',
          clickFlag:true
        })
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        })
      }
    })
    //监听上传进度变化事件
    uploadTask.onProgressUpdate((res) =>{
      wx.showLoading({
        title: '上传进度：'+res.progress+'%',
        mask: true //是否显示透明蒙层，防止触摸穿透
      })
      console.log("上传进度",res.progress)
      console.log("已经上传的数据长度，单位 Bytes:",res.totalBytesSent)
      console.log("预期需要上传的数据总长度，单位 Bytes:",res.totalBytesExpectedToSend)
    })
  },



// 选择图片显示函数（不上传，用于四角照）
  upload2: function (e) {
    console.log("upload")
    let that = this
    wx.chooseImage({
      success: function (res) {
        // console.log(res)
        let tmpFile = res.tempFilePaths[0]
        that.setData({
          img_url2: tmpFile
        })
        that.setData({
          isLoading2: true
        })
      },
    })
  },
// 选择图片显示函数（不上传，用于四角照）
  upload3: function (e) {
    console.log("upload")
    let that = this
    wx.chooseImage({
      success: function (res) {
        // console.log(res)
        let tmpFile = res.tempFilePaths[0]
        that.setData({
          img_url3: tmpFile
        })
        that.setData({
          isLoading3: true
        })

      },
    })
  },
// 选择图片显示函数（不上传，用于四角照）
  upload4: function (e) {
    console.log("upload")
    let that = this
    wx.chooseImage({
      success: function (res) {
        // console.log(res)
        let tmpFile = res.tempFilePaths[0]
        that.setData({
          img_url4: tmpFile
        })
        that.setData({
          isLoading4: true
        })
      },
    })
  },
  // 页面跳转函数
  // 跳转结果界面
  tapToRes: function(e){
    wx.navigateTo({
      url: '../result/result',
    })
  },
// 跳转函数
  // 跳转到main界面(只能用switchTab)
  taptomain: function (e) {
    wx:wx.switchTab({
      url: '../main/main',
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {},
    })
  }
})