// pages/result/result.js
// 初始化实例
import * as echarts from "../../ec-canvas/echarts";

var app = getApp();
function setOption(chart, linedata, point1data, point2data) {
    const option = {
        title: {
            show: true, //显示策略，默认值true,可选为：true（显示） | false（隐藏）
            text: '闭眼检测中的ear值', //主标题文本，'\n'指定换行 
            subtext: '该值反映闭眼水平，值越小表明人眼闭合程度越小', //副标题文本，'\n'指定换行 
            x: 'center', //水平
            textStyle: { //主标题文本样式{"fontSize": 18,"fontWeight": "bolder","color": "#333"} 
                fontFamily: 'Arial, Verdana, sans...',
                fontSize: 20,
                fontStyle: 'normal',
                fontWeight: 'normal',
                color: '#ffffff',
            },
        },
        color: ['#37A2DA', '#e06343', '#37a354', '#b55dba', '#b5bd48', '#8378EA', '#96BFFF'],
        legend: {
            data: ["ear value", "blink status", "close status"],
            top: 20,
            left: "center",
            textStyle: {//图例文字的样式
                color: '#ffffff',
            },
            z: 1000
        },
        grid: {
            left: '3%',
            right: '5%',
            bottom: '5%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: false,
            name: 'time(s)',
            nameTextStyle: {
                padding: [60, 0, 0, -50]    // 四个数字分别为上右下左与原位置距离
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
        yAxis: {
            x: 'center',
            type: 'value',
            name: 'ear',
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
            name: 'ear value',
            type: 'line',
            smooth: true,
            symbol: 'none',  //取消折点圆圈
            data: linedata
        }, {
            name: 'blink status',
            type: 'scatter',
            itemStyle: {
                normal: {
                    color: '#F4CB29', //折线点颜色
                },
            },
            data: point1data,
            z: 100
        }, {
            name: 'close status',
            type: 'scatter',
            itemStyle: {
                normal: {
                    color: '#DC143C', //折线点颜色
                },
            },
            data: point2data,
            z: 200
        }
        ]
    };
    chart.setOption(option)
}

Page({
    data: {
        tabs: ["闭眼检测", "头部姿态检测", "不规范行为检测", "视线检测"],
        jsondata: {},
        ResVideoPath: "",
        total: 0,
        category: "",
        interttime: "",
        ec: {
            lazyLoad: true
        }
    },
  // 页面载入函数
  // 捕获globalData中的结果信息
    // 初次进入拍照时，如无上传，则请求返回上传
    onLoad: function (options) {
        var that = this;
        var jsondata = JSON.parse(JSON.parse(decodeURIComponent(options.jsondata)));

        that.setData({
            jsondata: jsondata,
            ResVideoPath: jsondata['videopath'],
            category: jsondata['category'],
            createtime: jsondata['inserttime'],
        })
        console.log("视频的地址为：")
        console.log(that.data.ResVideoPath)
    },
    // onReady: function (options) {
    //     var that = this;
    //     that.oneComponent = that.selectComponent('#mychart-dom-line');
    //     var linedata = [];
    //     var point1data = [];
    //     var point2data = [];
    //     for (let i = 0, len = that.data.jsondata['time'].length; i < len; i++) {
    //         linedata.push([that.data.jsondata['time'][i], that.data.jsondata['ear'][i]]);
    //         if (that.data.jsondata['status'][i] == 1) {
    //             point1data.push([that.data.jsondata['time'][i], that.data.jsondata['ear'][i]]);
    //         } else if (that.data.jsondata['status'][i] == 2) {
    //             point2data.push([that.data.jsondata['time'][i], that.data.jsondata['ear'][i]]);
    //         }
    //     }
    //     this.init_one(linedata, point1data, point2data);
    // },

    // init_one: function (linedata, point1data, point2data) {           //初始化第一个图表
    //     this.oneComponent.init((canvas, width, height) => {
    //         const chart = echarts.init(canvas, null, {
    //             width: width,
    //             height: height
    //         });
    //         setOption(chart, linedata, point1data, point2data);
    //         this.chart = chart;
    //         return chart;
    //     });
    // },

    //返回主页
    retToMain: function (e) {
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
