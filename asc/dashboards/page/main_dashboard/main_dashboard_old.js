frappe.pages['main-dashboard'].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'Main Dashboard',
    single_column: true
  });

  $(frappe.render_template("main_dashboard", { doc: 4444 })).appendTo(
    page.main
  );

  highchartstack();
  columnchart();
  chartpie();
  chartpie2();
  columnchart2();
  columnchart3();
  piefunc();
  filters.add(page);
}

filters = {
  add: function (page) {
    let year = page.add_field({
      label: "Year",
      fieldtype: "Link",
      fieldname: "Year",
      options: "Year",
      reqd: 1,
    });
    let district = page.add_field({
      label: "District",
      fieldtype: "Link",
      fieldname: "district",
      options: "District",
    });
    let fiterbtn = page.add_field({
      label: "View",
      fieldtype: "Button",
      fieldname: "filter",
      click() {
        $(".abc").empty();
        $(frappe.render_template("main_dashboard", { doc: 1234 })).appendTo(page.main);
        //filters.add(page);
        //columnchart2();
        // columnchart3();
        /*frappe.call({
          method: "asc.dashboards.page.main_dashboard.main_dashboard.get_data",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            console.log(r.message);
           
            );
          },
        });*/
      },
    });
  },
};


function highchartstack() {
  Highcharts.chart('container', {
    chart: {
      type: 'bar'
    },
    colors: ['#ffc415', '#0091F7', '#F740A9'],
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },
    title: {
      text: '',
      align: 'left',
      x: 105
    },
    xAxis: {
      categories: ['Primary', 'Middle', 'Elementary', 'Secondary', 'Higher Secondary']
    },
    yAxis: {
      min: 0,
      title: {
        text: ''
      }
    },
    legend: {
      reversed: true
    },
    plotOptions: {
      series: {
        stacking: 'normal',
        dataLabels: {
          enabled: true
        }
      }
    },
    series: [{
      name: 'Mixed',
      data: [31116, 31116, 31116, 31116, 31116]
    }, {
      name: 'Boys',
      data: [7712, 7712, 7712, 7712, 7712]
    }, {
      name: 'Girls',
      data: [5468, 7712, 7712, 7712, 7712]
    }]
  });
}

function pietychart1() {
  $(".donut-mini-1").peity("donut", {
    fill: ["#FF5858"],
    width: "95",
    height: "95",
    innerRadius: "35",


  });
}
function pietychart2() {
  $(".donut-mini-2").peity("donut", {
    fill: ["#3F5374"],
    width: "95",
    height: "95",
    innerRadius: "35",


  });
}
function pietychart3() {
  $(".donut-mini-3").peity("donut", {
    fill: ["#FFA62E"],
    width: "95",
    height: "95",
    innerRadius: "35",


  });
}

function columnchart() {
  Highcharts.chart('containercol', {
    chart: {
      type: 'column'
    },
    colors: [
      '#F75C1E',
      '#85C9E8',
      '#0000ff',
      '#ABF7F7'
    ],
    title: {
      text: ''
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },

    xAxis: {
      categories: [
        'Primary',
        'Middle',
        'Elementary',
        'Secondary',
        'Higher Secondary'
      ],
      crosshair: true
    },
    yAxis: {
      min: 0,
      title: {
        text: ''
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      series: {
        borderRadius: 4,
        pointPadding: 3.2,
      },
      column: {
        pointPadding: 0.2,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    series: [{
      name: 'Urdu',
      data: [49.9, 71.5, 106.4, 129.2, 144.0]

    }, {
      name: 'Sindhi',
      data: [83.6, 78.8, 98.5, 93.4, 106.0]

    }, {
      name: 'English',
      data: [48.9, 38.8, 39.3, 41.4, 47.0]

    }, {
      name: 'Mixed',
      data: [42.4, 33.2, 34.5, 39.7, 52.6,]

    }]
  });

}


function chartpie() {
  Highcharts.chart('containerpie', {
    chart: {
      type: 'variablepie'
    },
    plotOptions: {
      pie: {
        size: 70,
        dataLabels: {
          enabled: true,
          color: '#000',
          format: '{point.name}',
          distance: -25,
          style: {
            fontSize: '20px',
            textOutline: 0
          },
        },
      },


    },
    colors: [
      '#E24C4C',
      '#F740A9',
      '#0091F7'
    ],
    title: {
      text: 'In Urban'
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>' +
        'Population: <b>{point.y}</b><br/>' +
        'Percentage: <b>{point.z}%</b><br/>'
    },
    series: [{
      minPointSize: 10,
      innerSize: '20%',
      zMin: 0,
      name: 'gender',

      data: [{
        name: 'Mixed',
        y: 3171,
        z: 61
      }, {
        name: 'Girls',
        y: 994,
        z: 19
      }, {
        name: 'Boys',
        y: 1012,
        z: 20
      }],

    }]
  });

}

function chartpie2() {
  Highcharts.chart('containerpie2', {
    chart: {
      type: 'variablepie'
    },
    plotOptions: {
      pie: {
        size: 70,
      }
    },
    colors: [
      '#FFC415',
      '#F740A9',
      '#0091F7'
    ],
    title: {
      text: 'In Rural'
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>' +
        'Population: <b>{point.y}</b><br/>' +
        'Percentage: <b>{point.z}%</b><br/>'
    },


    series: [{
      minPointSize: 10,
      innerSize: '20%',
      zMin: 0,
      name: 'gender',
      data: [{
        name: 'Mixed',
        y: 3171,
        z: 61
      }, {
        name: 'Girls',
        y: 994,
        z: 19
      }, {
        name: 'Boys',
        y: 1012,
        z: 20
      }],

    }]
  });

}


function columnchart2() {
  Highcharts.chart('containergender', {
    chart: {
      type: 'bar'
    },
    colors: ['#0091F7', '#F740A9'],
    title: {
      text: 'Class and Gender wise Enrollments'
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },

    xAxis: {
      categories: [
        'Kachi',
        'Class I',
        'Class II',
        'Class II',
        'Class IV',
        'Class V',
        'Class VI',
        'Class VII',
        'Class VIII',
        'Class IX',
        'Class X',
        'Class XI',
        'Class XII'
      ],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: '',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ' millions'
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 80,
      floating: true,
      borderWidth: 1,
      backgroundColor:
        Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: 'Boys',
      data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4, 40]

    }, {
      name: 'Girls',
      data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3, 90]

    }]
  });
}

function columnchart3() {
  Highcharts.chart('containerteacher', {
    chart: {
      type: 'bar'
    },
    colors: [
      '#FFC107',
      '#0D6EFD'

    ],
    title: {
      text: 'Designation and Gender wise Teachers'
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },

    xAxis: {
      categories: [
        'Primary School Teacher',
        'Junior Elementary School Teacher',
        'High School Teacher',
        'Subject Specialistr',
        'Physical Training Instructor',
        'Workshop Instructor Teacher',
        'Head Master / Mistress',
        'Drawing Teacher',
        'Others',
        '*Non-Government Teacher',
        'No Info'],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: '',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ' millions'
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 80,
      floating: true,
      borderWidth: 1,
      backgroundColor:
        Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: 'Female Teacher',
      data: [107, 31, 635, 203, 20, 107, 31, 635, 203, 50, 66]
    }, {
      name: 'Male Teacher',
      data: [133, 156, 947, 408, 68, 133, 156, 947, 408, 90, 65]
    }]
  });
}


function piefunc() {
  Highcharts.chart('containerpiefunc', {
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
    },
    colors: ['#008140', '#F70000'],
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false
    },
    title: {
      text: '',
      y: 24
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
      point: {
        valueSuffix: '%'
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        }
      }
    },
    series: [{
      name: 'Brands',
      colorByPoint: true,
      data: [{
        name: 'Functional',
        y: 61.41,
        sliced: true,
        selected: true
      }, {
        name: 'Non-functional',
        y: 11.84
      }]
    }]
  });
}
