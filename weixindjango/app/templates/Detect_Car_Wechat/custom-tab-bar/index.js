const app = getApp();
Component({
  //数据
  data: {
    selected: 2,//当前tabBar页面
    color: "#cdcdcd",//未选中tabBar时的文字颜色
    selectedColor: "#22385d",//选中时tabBar文字颜色
    addImgPath:'/pages/picture/cam.png',//添加发布图标
    // tabBar对象集合
    list: [
      {
        pagePath: "/pages/lipei/lipei",
        iconPath: "/pages/picture/record.png",
        selectedIconPath: "/pages/picture/record_clicked.png",
        text: "理赔"
      },
      {
        pagePath: "/pages/perInfo/perInfo",
        iconPath: "/pages/picture/me-n.png",
        selectedIconPath: "/pages/picture/me_clicked.png",
        text: "我的"
      },
      {
        pagePath: "/pages/main/main",
        iconPath: "/pages/picture/cam.png",
        selectedIconPath: "/pages/picture/cam.png",
        text: "相机"
      }
    ]
  },
  methods: {
    // tabBar切换事件
    tab_bar_index(e) {
      const url = e.currentTarget.dataset.path
      console.log(url)
      wx.switchTab({url})
    },

    // 发布添加按钮跳转
    tab_bar_add(e) {
      if(this.data.selected===2){  //2 代表主界面
        var url = "/pages/sc/sc"
        wx.navigateTo({ url })
      }
      else{    //否则转回主界面
        const url = e.currentTarget.dataset.path
        console.log(url)
        wx.switchTab({ url:"/pages/main/main" })
      }
    }
  }
})