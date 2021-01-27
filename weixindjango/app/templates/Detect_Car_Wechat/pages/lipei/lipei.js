// pages/lipei/lipei.js
Component({
  pageLifetimes: {
    show() {
      this.getTabBar().setData({
        selected: 0
      });
    }
  },

    data: {
      status: ["block", "block", "block"],
      all_url:"https://lamaric.goho.co/media/icon/icon_all_orange.png",
      wait_url:"https://lamaric.goho.co/media/icon/icon_dailipei_old.png",
      notbaobao_url:"https://lamaric.goho.co/media/icon/icon_notbaobao_white.png",
      finish_url:"https://lamaric.goho.co/media/icon/icon_finish_green.png"

    },
  methods:{
    btn_all: function () {
      this.setData({
        status: ["block", "block", "block"],
        all_url: "https://lamaric.goho.co/media/icon/icon_all_orange.png",
        wait_url: "https://lamaric.goho.co/media/icon/icon_dailipei_old.png",
        notbaobao_url: "https://lamaric.goho.co/media/icon/icon_notbaobao_white.png",
        finish_url: "https://lamaric.goho.co/media/icon/icon_finish_green.png"
      })
    },
    btn_wait: function () {
      this.setData({
        status: ["block", "none", "none"],
        all_url: "https://lamaric.goho.co/media/icon/icon_all_white.png",
        wait_url: "https://lamaric.goho.co/media/icon/icon_dailipei_point.png",
        notbaobao_url: "https://lamaric.goho.co/media/icon/icon_notbaobao_white.png",
        finish_url: "https://lamaric.goho.co/media/icon/icon_finish_green.png"
      })
    },
    btn_notinsure: function () {
      this.setData({
        status: ["none", "block", "none"],
        all_url: "https://lamaric.goho.co/media/icon/icon_all_white.png",
        wait_url: "https://lamaric.goho.co/media/icon/icon_dailipei_old.png",
        notbaobao_url: "https://lamaric.goho.co/media/icon/icon_notbaobao_orange.png",
        finish_url: "https://lamaric.goho.co/media/icon/icon_finish_green.png"
      })
    },
    btn_finish: function () {
      this.setData({
        status: ["none", "none", "block"],
        all_url: "https://lamaric.goho.co/media/icon/icon_all_white.png",
        wait_url: "https://lamaric.goho.co/media/icon/icon_dailipei_old.png",
        notbaobao_url: "https://lamaric.goho.co/media/icon/icon_notbaobao_white.png",
        finish_url: "https://lamaric.goho.co/media/icon/icon_finish_orange.png"
      })
    },
  }


  })
  