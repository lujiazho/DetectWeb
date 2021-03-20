/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  var ctx_inc = document.getElementById('myChart_increase')
  var seven_days= Server.seven_days
  var thirty_days= Server.thirty_days
  var whole_year= Server.whole_year
  var ten_year = Server.ten_year
  // eslint-disable-next-line no-unused-vars
  if(seven_days !== -1){
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          '近一周',
          '近六日',
          '近五日',
          '近四日',
          '近三日',
          '近二日',
          '近一日'
        ],
        datasets: [{
          data: seven_days,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })
    for (let i=0; i<seven_days.length; i++){
      if(i!=seven_days.length-1){
        seven_days[i] = seven_days[i] - seven_days[i+1]
      }else{
        seven_days[i] = seven_days[i]
      }
    }
    var colorList = new Array(7)

    for (let i=0; i<seven_days.length; i++){
      if (seven_days[i] >= 20){
        colorList[i] = '#C1232B'
      }else if (seven_days[i] >= 15){
        colorList[i] = '#D7504B'
      }else if (seven_days[i] >= 10){
        colorList[i] = '#FE8463'
      }else if (seven_days[i] >= 5){
        colorList[i] = '#C6E579'
      }
    }
    var myChart_increase = new Chart(ctx_inc, {
      type: 'bar',
      data: {
        labels: [
          '一周前',
          '六日前',
          '五日前',
          '四日前',
          '三日前',
          '二日前',
          '一日前'
        ],
        datasets: [{
          data: seven_days,
          borderSkipped:"bottom",//默认为底部
          backgroundColor: colorList,
          borderColor: colorList,
          borderWidth: 1,
        }]
      },
      options: {
        legend: {
          display: false
        }
      }
    })
  }else if(thirty_days !== -1){
    var label = new Array(30)
    for (let i=0; i<label.length; i++){
      label[i] = (30-i).toString()+"天内"
    }
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: label,
        datasets: [{
          data: thirty_days,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })
    // 30天 每日新增
    for (let i=0; i<label.length; i++){
      label[i] = (30-i).toString()+"天前"
    }
    for (let i=0; i<thirty_days.length; i++){
      if(i!=thirty_days.length-1){
        thirty_days[i] = thirty_days[i] - thirty_days[i+1]
      }else{
        thirty_days[i] = thirty_days[i]
      }
    }
    var colorList = new Array(30)

    for (let i=0; i<thirty_days.length; i++){
      if (thirty_days[i] >= 20){
        colorList[i] = '#C1232B'
      }else if (thirty_days[i] >= 15){
        colorList[i] = '#D7504B'
      }else if (thirty_days[i] >= 10){
        colorList[i] = '#FE8463'
      }else if (thirty_days[i] >= 5){
        colorList[i] = '#C6E579'
      }
    }
    var myChart_increase = new Chart(ctx_inc, {
      type: 'bar',
      data: {
        labels: label,
        datasets: [{
          data: thirty_days,
          borderSkipped:"bottom",//默认为底部
          backgroundColor: colorList,
          borderColor: colorList,
          borderWidth: 1,
        }]
      },
      options: {
        legend: {
          display: false
        }
      }
    })
  }else if(whole_year !== -1){
    // 参考https://www.chartjs.org/docs/latest/charts/bar.html
    var label = new Array(12)
    var colorList = new Array(12)
    for (let i=0; i<label.length; i++){
      label[i] = (12-i).toString()+"月内"
    }
    for (let i=0; i<label.length; i++){
      if (whole_year[i] > 20){
        colorList[i] = '#C1232B'
      }else if (whole_year[i] > 15){
        colorList[i] = '#D7504B'
      }else if (whole_year[i] > 10){
        colorList[i] = '#FE8463'
      }else if (whole_year[i] > 5){
        colorList[i] = '#C6E579'
      }
    }
    // var colorList = [
    //                    '','#B5C334','#FCCE10','#E87C25','#27727B',
    //                    '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
    //                    '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
    //                 ];
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: label,
        datasets: [{
          data: whole_year,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })

    // 年 每月新增
    for (let i=0; i<label.length; i++){
      label[i] = (12-i).toString()+"月前"
    }
    for (let i=0; i<whole_year.length; i++){
      if(i!=whole_year.length-1){
        whole_year[i] = whole_year[i] - whole_year[i+1]
      }else{
        whole_year[i] = whole_year[i]
      }
    }
    var colorList = new Array(12)

    for (let i=0; i<whole_year.length; i++){
      if (whole_year[i] >= 20){
        colorList[i] = '#C1232B'
      }else if (whole_year[i] >= 15){
        colorList[i] = '#D7504B'
      }else if (whole_year[i] >= 10){
        colorList[i] = '#FE8463'
      }else if (whole_year[i] >= 5){
        colorList[i] = '#C6E579'
      }
    }
    var myChart_increase = new Chart(ctx_inc, {
      type: 'bar',
      data: {
        labels: label,
        datasets: [{
          data: whole_year,
          borderSkipped:"bottom",//默认为底部
          backgroundColor: colorList,
          borderColor: colorList,
          borderWidth: 1,
        }]
      },
      options: {
        legend: {
          display: false
        }
      }
    })
  }else{ // 最近十年
    // 参考https://www.chartjs.org/docs/latest/charts/bar.html
    var label = new Array(10)
    var colorList = new Array(10)
    for (let i=0; i<label.length; i++){
      label[i] = (10-i).toString()+"年内"
    }
    // var colorList = [
    //                    '','#B5C334','#FCCE10','#E87C25','#27727B',
    //                    '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
    //                    '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
    //                 ];
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: label,
        datasets: [{
          data: ten_year,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })

    // 十年 每年新增
    for (let i=0; i<label.length; i++){
      label[i] = (10-i).toString()+"年前"
    }
    for (let i=0; i<ten_year.length; i++){
      if(i != ten_year.length-1){
        ten_year[i] = ten_year[i] - ten_year[i+1]
      }else{
        ten_year[i] = ten_year[i]
      }
    }
    var colorList = new Array(10)

    for (let i=0; i<ten_year.length; i++){
      if (ten_year[i] >= 200){
        colorList[i] = '#C1232B'
      }else if (ten_year[i] >= 150){
        colorList[i] = '#D7504B'
      }else if (ten_year[i] >= 100){
        colorList[i] = '#FE8463'
      }else if (ten_year[i] >= 50){
        colorList[i] = '#C6E579'
      }
    }
    var myChart_increase = new Chart(ctx_inc, {
      type: 'bar',
      data: {
        labels: label,
        datasets: [{
          data: ten_year,
          borderSkipped:"bottom",//默认为底部
          backgroundColor: colorList,
          borderColor: colorList,
          borderWidth: 1,
        }]
      },
      options: {
        legend: {
          display: false
        }
      }
    })
  }

})()
