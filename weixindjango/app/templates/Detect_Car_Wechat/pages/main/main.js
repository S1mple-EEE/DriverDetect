// pages/main/main.js
const app=getApp()
Page({

  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },

// redirectTo：关闭当前页(卸载) ，跳转到指定页

// navigateTo：保留当前页(隐藏) ，跳转到指定页

// switchTap：只能用于跳转到tabbar页面，并关闭其他非tabbar页面, tabbar之间做切换
  onLoad: function() {
    // 查看是否授权
    wx.getSetting({
      success: function(res){
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: function(res) {
              console.log(res.userInfo)
              //用户已经授权过
            }
          })
        }
      }
    })
  },
  // 页面跳转函数
  // 跳转到上传图片界面
  jumppage:function(e) {
    wx:wx.navigateTo({
      url: '../sc/sc',
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {},
    })
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    console.log(app.globalData.userInfo )
  }
  
})