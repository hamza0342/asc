frappe.pages['asc-tracker'].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'ASC Tracker',
    single_column: true
  });
  $(frappe.render_template("asc_tracker")).appendTo(page.main);
  frappe.call({
    method: "asc.dashboards.page.asc_tracker.asc_tracker.page_query",
    freeze: true,
    callback: function (r) {
      set.values(r)
      columnchart(r.message.district_names, r.message.per_dict, r.message.district_images);
      piechart(r.message.school_level);
    },
  });
  setInterval(async () => {
    await frappe.call({
      method: "asc.dashboards.page.asc_tracker.asc_tracker.page_query",
      callback: function (r) {
        set.values(r)
        columnchart(r.message.district_names, r.message.per_dict, r.message.district_images);
        piechart(r.message.school_level);
      },
    });
  }, 20000);
}
filters = {
  add: function (page) {
    // frappe.call({
    // 	method: "asc.dashboards.page.asc_tracker_dummy.asc_tracker_dummy.page_query",
    //   freeze:true,
    // 	callback: function (r) {
    //     console.log(r.message);
    // 		set.values(r)
    //     columnchart(r.message.district_names, r.message.per_dict, r.message.district_images);
    //     piechart(r.message.school_level);
    // 	},
    // });
  },
}
set = {
  values: function (r) {
    make_page.total_schools(r.message.total_schools);
    make_page.entered_asc_schools(r.message.stack.entered_asc_schools, r.message.total_schools);
    make_page.fun_asc_school(r.message.stack.func_asc_schools, r.message.stack.entered_asc_schools);
    make_page.close_asc_school(r.message.stack.closed_asc_schools, r.message.stack.entered_asc_schools);
    make_page.completed_asc(r.message.stack.entered_asc_schools);
    make_page.school_no_building(r.message.stack.schools_no_building, r.message.stack.entered_asc_schools);
    make_page.total_student_enrollment(r.message.total_enrol);
    make_page.school_no_electricity(r.message.stack.schools_no_electricity, r.message.stack.entered_asc_schools);
    make_page.total_single_teacher_school(r.message.stack.schools_single_teacher, r.message.stack.entered_asc_schools);
    make_page.school_no_water(r.message.stack.schools_no_water, r.message.stack.entered_asc_schools);
    make_page.total_staff(r.message.total_staff);
    make_page.total_upload_images(r.message.total_images);
  }
}
make_page = {
  total_schools: function (total_schools) {
    $("#total_schools").empty();
    $("#total_schools").html(total_schools.toLocaleString("en-US"));
  },
  entered_asc_schools: function (entered_asc_schools, total_schools) {
    $("#entered_asc_schools").empty();
    $("#entered_asc_schools").html(entered_asc_schools.toLocaleString("en-US"))
    const asc_per = entered_asc_schools / total_schools * 100
    const value = `(${asc_per.toFixed(0)}%)`
    $("#asc_percentage").empty();
    $("#asc_percentage").html(value);
  },
  fun_asc_school: function (fun_asc_school, total_schools) {
    $("#fun_asc_school").empty();
    $("#fun_asc_school").html(fun_asc_school.toLocaleString("en-US"));
    const fun_per = fun_asc_school / total_schools * 100
    const fun_value = `(${fun_per.toFixed(0)}%)`
    $("#fun_percentage").empty();
    $("#fun_percentage").html(fun_value);
  },
  close_asc_school: function (close_asc_school, total_schools) {
    $("#close_asc_school").empty();
    $("#close_asc_school").html(close_asc_school.toLocaleString("en-US"));
    const close_per = close_asc_school / total_schools * 100
    const close_value = `(${close_per.toFixed(0)}%)`
    $("#close_percentage").empty();
    $("#close_percentage").html(close_value);
  },
  completed_asc: function (completed_asc) {
    $("#completed_asc").empty();
    $("#completed_asc").html(completed_asc.toLocaleString("en-US"));
  },
  school_no_building: function (school_no_building, entered_asc_schools) {
    $("#school_no_building").empty();
    $("#school_no_building").html(school_no_building.toLocaleString("en-US"));
    const close_per = school_no_building / entered_asc_schools * 100
    const close_value = `(${close_per.toFixed(0)}%)`
    $("#no_building_percentage").empty();
    $("#no_building_percentage").html(close_value);
  },
  total_student_enrollment: function (total_student_enrollment) {
    $("#total_student_enrollment").empty();
    $("#total_student_enrollment").html(total_student_enrollment.toLocaleString("en-US"));
  },
  school_no_electricity: function (school_no_electricity, entered_asc_schools) {
    $("#school_no_electricity").empty();
    $("#school_no_electricity").html(school_no_electricity.toLocaleString("en-US"));
    const close_per = school_no_electricity / entered_asc_schools * 100
    const close_value = `(${close_per.toFixed(0)}%)`
    $("#no_electricity_percentage").empty();
    $("#no_electricity_percentage").html(close_value);
  },
  total_single_teacher_school: function (total_single_teacher_school, entered_asc_schools) {
    $("#total_single_teacher_school").empty();
    $("#total_single_teacher_school").html(total_single_teacher_school.toLocaleString("en-US"));
    const close_per = total_single_teacher_school / entered_asc_schools * 100
    const close_value = `(${close_per.toFixed(0)}%)`
    $("#single_teacher_percentage").empty();
    $("#single_teacher_percentage").html(close_value);
  },
  school_no_water: function (school_no_water, entered_asc_schools) {
    $("#school_no_water").empty();
    $("#school_no_water").html(school_no_water.toLocaleString("en-US"));
    const water_per = school_no_water / entered_asc_schools * 100
    const water_value = `(${water_per.toFixed(0)}%)`
    $("#no_water_percentage").empty();
    $("#no_water_percentage").html(water_value);
  },
  total_staff: function (total_staff) {
    $("#total_staff").empty();
    $("#total_staff").html(total_staff.toLocaleString("en-US"));
  },
  total_upload_images: function (total_images) {
    $("#total_upload_images").empty();
    $("#total_upload_images").html(total_images.toLocaleString("en-US"));
  },
}

function columnchart(district_names, district_asc, district_images) {
  Highcharts.chart('container1', {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Data Entry Completion Status District Wise'
    },
    subtitle: {
      text: ''
    },
    xAxis: {
      categories: district_names,
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
        '<td style="padding:0"><b>{point.y:.1f}%</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0,
        // stacking: 'percent',
        dataLabels: {
          enabled: true
        }
      }
    },
    series: [{
      name: 'ASC',
      data: district_asc
    }, {
      name: 'Images',
      data: district_images

    }]
  });
  // 	Highcharts.chart('container1', {
  //     chart: {
  //         type: 'column'
  //     },
  // 	  colors: ["#0162e8", "#00cccc", "#673ab7", "#00b9ff"],
  //     title: {
  //         text: 'Data entry Completion Status District wise',
  // 		align: 'left',
  // 		 x: 30,
  // 		  style: {

  //             fontWeight: 'bold'
  //         }
  //     },
  //      credits: {
  //       enabled: false,
  //     },
  //     exporting: {
  //       enabled: false,
  //     },
  // 	 plotOptions: {
  //         series: {
  //             pointWidth: 20
  //         }
  //     },
  //     subtitle: {
  //         text: ''
  //     },
  //     xAxis: {
  //         type: 'category',
  //         labels: {
  //             rotation: -45,
  //             style: {
  //                 fontSize: '12px',
  //                 fontFamily: 'Roboto',
  //             }
  //         }
  //     },
  //     yAxis: {
  //         min: 0,

  //     },
  //     legend: {
  //         enabled: false
  //     },
  //     tooltip: {
  //         pointFormat: 'Progress: <b>{point.y:.0f} Schools</b>'
  //     },
  //     series: [{
  //         name: 'ASC',
  //         data: district_asc,
  //         dataLabels: {
  //             enabled: true,
  //             rotation: -90,
  //             color: '#FFFFFF',
  //             align: 'right',
  //             format: '{point.y:.0f}', // one decimal
  //             y: 10, // 10 pixels down from the top
  //             style: {
  //                 fontSize: '10px',
  //                 fontFamily: 'Roboto',
  //             }
  //         }
  //     }]
  // });
}

function piechart(school_level) {
  // Make monochrome colors
  var pieColors = (function () {
    var colors = [],
      base = Highcharts.getOptions().colors[0],
      i;

    for (i = 0; i < 10; i += 1) {
      // Start out with a darkened base color (negative brighten), and end
      // up with a much brighter color
      colors.push(Highcharts.color(base).brighten((i - 2) / 7).get());
    }
    return colors;
  }());
  let data = []
  for (let i = 0; i < school_level.length; i++) {
    obj = {}
    const element = school_level[i];
    obj = { name: element[0], y: element[1] }
    data.push(obj)
  }
  // Build the chart
  Highcharts.chart('container2', {
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
    },

    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    title: {
      text: ''

    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.0f}%</b>'
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
        colors: pieColors,
        center: [150, 98],
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b><br>{point.percentage:.0f} %',
          distance: -50,
          filter: {
            property: 'percentage',
            operator: '>',
            value: 4
          }
        }
      }
    },
    series: [{
      name: 'Schools',
      data: data
    }]
  });
}
