// pages/result/result.js
// 初始化实例
var app=getApp();

Page({
  data: {
    jsondata:{},
    ResVideoPath:"",
    resimg: "",             //结果图片地址
    result: "",             //结果文本地址
    haveres:"",             //布尔判断
    atten:"检测结果查看",
    total: 0,
  },
  // 页面载入函数
  // 捕获globalData中的结果信息
  // 初次进入拍照时，如无上传，则请求返回上传
  onLoad: function (options) {
    var that = this;
    var jsondata= JSON.parse(JSON.parse(decodeURIComponent(options.jsondata)));
    that.data.jsondata=jsondata;
    that.setData({
      ResVideoPath:jsondata['videopath']
    })
    
    that.data.resimg = app.globalData.resultimg;
    that.data.result = app.globalData.resultfinally;
    if (that.data.result === null) {
      that.data.haveres = false;
    } else {
      that.data.haveres = true;
      that.setData({
        haveres: that.data.haveres,
        resimg: that.data.resimg,
        result: that.data.result
      })
    }
  },
  //返回主页
  retToMain:function(e){
    // console.log('ljsdafj')
    wx:wx.switchTab({
      url: '../main/main',
    })
  },
  //预览图片
  previewImg:function(event){
    var that = this;
    var src = that.data.resimg;
    wx.previewImage({
      current: src,
      urls: [src],
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {},
    })
    },
  //获取选中的checkbox的value  value=price
  checkboxChange: function (e) {
    var that = this;
    var selected = 0;
    // console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    for (var j = 0, len = e.detail.value.length; j < len; j++) {
      // console.log(parseInt(e.detail.value[j]));
      selected += parseInt(e.detail.value[j]);
    }
    // console.log(selected);
    that.setData({total: selected})

  },
  // 跳转函数
  // 跳转到上传图片界面
  taptosc: function(e){
    wx.navigateTo({
      url: '../sc/sc',
    })
  }
})
