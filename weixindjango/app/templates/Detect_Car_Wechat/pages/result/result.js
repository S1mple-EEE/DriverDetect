// pages/result/result.js
// 初始化实例
import * as echarts from "../../ec-canvas/echarts";

var app = getApp();

function initChart(canvas, width, height) {
    const chart = echarts.init(canvas, null, {
        width: width,
        height: height
    });
    canvas.setChart(chart);

    var option = {
        color: ["#37A2DA", "#67E0E3", "#9FE6B8"],
        legend: {
            data: ["A", "B", "C"],
            top: 20,
            left: "center",
            textStyle: {//图例文字的样式
                color: '#ffffff',
            },
            z: 100

        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            axisLabel: {
                textStyle: {
                    color: '#ffffff',  //坐标的字体颜色
                },
            },
            axisLine: {
                lineStyle: {
                    color: '#ffffff',  //坐标轴的颜色
                },
            },

        },
        yAxis: {
            x: 'center',
            type: 'value',
            splitLine: {
                lineStyle: {
                    type: 'solid'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#ffffff',  //坐标的字体颜色
                },
            },
            axisLine: {
                lineStyle: {
                    color: '#ffffff',  //坐标轴的颜色
                },
            },
        },
        series: [{
            name: 'A',
            type: 'line',
            smooth: true,
            data: [18, 36, 65, 30, 78, 40, 33]
        },
            {
                name: 'B',
                type: 'line',
                smooth: true,
                data: [12, 50, 51, 35, 70, 30, 20]
            },
            {
                name: 'C',
                type: 'line',
                smooth: true,
                data: [10, 30, 31, 50, 40, 20, 10]
            }
        ]
    };
    chart.setOption(option);
    return chart;
}

Page({
    data: {
        jsondata: {},
        ResVideoPath: "",
        resimg: "",             //结果图片地址
        result: "",             //结果文本地址
        haveres: "",             //布尔判断
        atten: "检测结果查看",
        total: 0,
        category: "",
        interttime: "",
        ec: {
            onInit: initChart
        }
    },
  // 页面载入函数
  // 捕获globalData中的结果信息
  // 初次进入拍照时，如无上传，则请求返回上传
  onLoad: function (options) {
    var that = this;
    var jsondata= JSON.parse(JSON.parse(decodeURIComponent(options.jsondata)));
    that.data.jsondata=jsondata;
    that.setData({
        ResVideoPath: jsondata['videopath'],
        category: jsondata['category'],
        createtime: jsondata['inserttime'],
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
  // 跳转函数
  // 跳转到上传图片界面
  taptosc: function(e){
    wx.navigateTo({
      url: '../sc/sc',
    })
  }
})
