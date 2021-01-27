// pages/perInfo/perInfo.js
const app = getApp()

Component({
  pageLifetimes: {
    show() {
      this.getTabBar().setData({
        selected: 1
      });
    }
  },
  attached: function () {
  },
  // 初始数据
  data: {
    img_url:"",   //储存头像
    name:""       //储存用户名
  },
  
  // 页面加载函数
  // 捕获数据
  onLoad: function () {
    var that=this;
    that.img_url = app.globalData.userInfo.avatarUrl
    that.name = app.globalData.userInfo.nickName
    this.setData({
      img_url: that.img_url,
      name: that.name
    })
  }
  
})