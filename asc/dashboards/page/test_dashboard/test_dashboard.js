frappe.pages["test-dashboard"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Test Dashboard",
    single_column: true,
  });
  // $(frappe.render_template("main_dashboard", { doc: 1111 })).appendTo(
  //   page.main
  // );

  // genderLevelPieChart();
  // MediumLevelChart);
  // locationGenderWisePieChartUrban();
  // locationGenderWisePieChartRural();
  // enrollmentChart();
  // teacherDesigGenderChart();
  // piefunc();

  filters.add(page);
};

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
        if (year.get_value() == "") {
          return;
        }
        $('#loader').remove();
        $('#test_dashboard').remove();
        var img = $('<img />', {
          id: 'loader',
          src: '/assets/img/loading.gif',
          alt: 'Loading',
          style: 'text-align:center; margin:0 auto; display:block'
        });
        img.appendTo(page.main);


        /*var img = $('<img />', { 
              id :'loader',
                src: '/assets/img/loading-image.gif',
                alt: 'Loading',
                style:'text-align:center'
              });
              img.appendTo(page.main);*/

        //$(img).appendTo(page.main);
        var genderLevelGraph_data;
        var enrollment_data;
        var location_gender_school;
        var medium_level_schools;
        var teachers_data;

        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.get_chart_data",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            genderLevelGraph_data = r.message;
          },
        });

        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.get_enrollment_data",

          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            enrollment_data = r.message;
          },
        });
        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.teachers_data",

          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            teachers_data = r.message;
            console.log(teachers_data);
          },
        });
        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.location_gender_schools",

          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            location_gender_school = r.message;
          },
        });
        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.medium_level_schools",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            medium_level_schools = r.message;
            console.log(medium_level_schools);
          },
        });
        frappe.call({
          method: "asc.dashboards.page.test_dashboard.test_dashboard.get_data",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            $('#test_dashboard').remove();
            $('#loader').remove();
            console.log("Data ", r.message);
            $(frappe.render_template("test_dashboard", r.message[0])).appendTo(
              page.main
            );
            $('#girls_prog').css('width', r.message[0].girls_percentage + '%')
            $('#boys_prog').css('width', r.message[0].boys_percentage + '%')
            $('#mixed_prog').css('width', r.message[0].mixed_percentage + '%')

            $('#primary_sat').css('width', r.message[0].Primary_Satisfactory_percentage + '%')
            $('#primary_repair').css('width', r.message[0].Primary_Needs_Repair_percentage + '%')
            $('#primary_dang').css('width', r.message[0].Primary_Dangerous_percentage + '%')
            $('#primary_rent').css('width', r.message[0].Primary_Rented_Others_percentage + '%')
            $('#primary_no_building').css('width', r.message[0].Primary_No_Building_Percentage + '%')



            $('#middle_sat').css('width', r.message[0].Middle_Elementary_Satisfactory_percentage + '%')
            $('#middle_repair').css('width', r.message[0].Middle_Elementary_Needs_Repair_percentage + '%')
            $('#midle_dang').css('width', r.message[0].Middle_Elementary_Dangerous_percentage + '%')
            $('#middle_rent').css('width', r.message[0].Middle_Elementary_Rented_Others_percentage + '%')
            $('#middle_no_building').css('width', r.message[0].Middle_Elementary_No_Building_percentage + '%')



            $('#sec_sat').css('width', r.message[0].Secondary_Satisfactory_percentage + '%')
            $('#sec_repair').css('width', r.message[0].Secondary_Needs_Repair_percentage + '%')
            $('#sec_dang').css('width', r.message[0].Secondary_Dangerous_percentage + '%')
            $('#sec_rent').css('width', r.message[0].Secondary_Rented_Others_percentage + '%')
            $('#sec_no_building').css('width', r.message[0].Secondary_No_Building_Percentage + '%')



            $('#high_sat').css('width', r.message[0].Higher_Secondary_Satisfactory_percentage + '%')
            $('#high_repair').css('width', r.message[0].Higher_Secondary_Needs_Repair_percentage + '%')
            $('#high_dang').css('width', r.message[0].Higher_Secondary_Dangerous_percentage + '%')
            $('#high_rent').css('width', r.message[0].Higher_Secondary_Rented_Others_percentage + '%')
            $('#high_no_building').css('width', r.message[0].Higher_Secondary_No_Building_Percentage + '%')





            genderLevelGraph(genderLevelGraph_data);
            MediumLevelChart(medium_level_schools);
            locationGenderWisePieChartUrban(location_gender_school);
            locationGenderWisePieChartRural(location_gender_school);
            enrollmentChart(enrollment_data);
            teacherDesigGenderChart(teachers_data);
            piefunc(r.message[1]);

          },
        });

      },
    });
  },
};

function genderLevelGraph(data) {
  var boys = Array(5).fill(0);
  var girls = Array(5).fill(0);
  var mixed = Array(5).fill(0);
  $.each(data[0], function (key, value) {
    if (key == "Primary_Boys") {
      boys[0] = value;
    } else if (key == "Middle_Boys") {
      boys[1] = value;
    } else if (key == "Elementary_Boys") {
      boys[2] = value;
    } else if (key == "Secondary_Boys") {
      boys[3] = value;
    } else if (key == "Higher_Secondary_Boys") {
      boys[4] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Primary_Girls") {
      girls[0] = value;
    } else if (key == "Middle_Girls") {
      girls[1] = value;
    } else if (key == "Elementary_Girls") {
      girls[2] = value;
    } else if (key == "Secondary_Girls") {
      girls[3] = value;
    } else if (key == "Higher_Secondary_Girls") {
      girls[4] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Primary_Mixed") {
      mixed[0] = value;
    } else if (key == "Middle_Mixed") {
      mixed[1] = value;
    } else if (key == "Elementary_Mixed") {
      mixed[2] = value;
    } else if (key == "Secondary_Mixed") {
      mixed[3] = value;
    } else if (key == "Higher_Secondary_Mixed") {
      mixed[4] = value;
    }
  });
  Highcharts.chart("container", {
    chart: {
      type: "bar",
    },
    colors: ["#ffc415", "#0091F7", "#F740A9"],
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    title: {
      text: "",
      align: "left",
      x: 105,
    },
    xAxis: {
      categories: [
        "Primary",
        "Middle",
        "Elementary",
        "Secondary",
        "Higher Secondary",
      ],
    },
    yAxis: {
      min: 0,
      title: {
        text: "",
      },
    },

    legend: {
      reversed: true,
    },
    plotOptions: {

      series: {
        stacking: "percent",
        dataLabels: {
          enabled: true,
          formatter: function () {
            if (this.y) {
              return this.y;
            }
          },
          position: "left",
          allowOverlap: true,
          crop: false,
          padding: 0,

        },
      },
    },

    series: [
      {
        name: "Mixed",
        data: mixed,
      },
      {
        name: "Boys",
        data: boys,
      },
      {
        name: "Girls",
        data: girls,
      },
    ],
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

function MediumLevelChart(data) {
  var urdu = Array(5).fill(0);
  var english = Array(5).fill(0);
  var sindth = Array(5).fill(0);
  var mixed = Array(5).fill(0);
  $.each(data[0], function (key, value) {
    if (key == "Primary_urdu_enrol") {
      urdu[0] = value;
    } else if (key == "Middle_urdu_enrol") {
      urdu[1] = value;
    } else if (key == "Elementary_urdu_enrol") {
      urdu[2] = value;
    } else if (key == "Secondary_urdu_enrol") {
      urdu[3] = value;
    } else if (key == "Higher_Secondary_urdu_enrol") {
      urdu[4] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Primary_english_enrol") {
      english[0] = value;
    } else if (key == "Middle_english_enrol") {
      english[1] = value;
    } else if (key == "Elementary_english_enrol") {
      english[2] = value;
    } else if (key == "Secondary_english_enrol") {
      english[3] = value;
    } else if (key == "Higher_Secondary_english_enrol") {
      english[4] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Primary_sindth_enrol") {
      sindth[0] = value;
    } else if (key == "Middle_sindth_enrol") {
      sindth[1] = value;
    } else if (key == "Elementary_sindth_enrol") {
      sindth[2] = value;
    } else if (key == "Secondary_sindth_enrol") {
      sindth[3] = value;
    } else if (key == "Higher_Secondary_sindth_enrol") {
      sindth[4] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Primary_mixed_enrol") {
      mixed[0] = value;
    } else if (key == "Middle_mixed_enrol") {
      mixed[1] = value;
    } else if (key == "Elementary_mixed_enrol") {
      mixed[2] = value;
    } else if (key == "Secondary_mixed_enrol") {
      mixed[3] = value;
    } else if (key == "Higher_Secondary_mixed_enrol") {
      mixed[4] = value;
    }
  });
  Highcharts.chart("containercol", {
    chart: {
      type: "column",
    },
    colors: ["#F75C1E", "#85C9E8", "#0000ff", "#ABF7F7"],
    title: {
      text: "",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },

    xAxis: {
      categories: [
        "Primary",
        "Middle",
        "Elementary",
        "Secondary",
        "Higher Secondary",
      ],
      crosshair: true,
    },
    yAxis: {
      min: 0,
      title: {
        text: "",
      },
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat:
        '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
      footerFormat: "</table>",
      shared: true,
      useHTML: true,
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
          enabled: true,

        },
      },
    },
    series: [
      {
        name: "Urdu",
        data: urdu,
      },
      {
        name: "Sindhi",
        data: sindth,
      },
      {
        name: "English",
        data: english,
      },
      {
        name: "Mixed",
        data: mixed,
      },
    ],
  });
}

function locationGenderWisePieChartUrban(data) {
  var urban = Array(10).fill(0);
  $.each(data[0], function (key, value) {
    if (key == "Urban_Boys") {
      urban[0] = parseInt(value);
    } else if (key == "Urban_Boys_percentage") {
      urban[1] = parseInt(value);
    } else if (key == "Urban_Girls") {
      urban[2] = parseInt(value);
    } else if (key == "Urban_Girls_percentage") {
      urban[3] = parseInt(value);
    } else if (key == "Urban_Mixed") {
      urban[4] = parseInt(value);
    } else if (key == "Urban_Mixed_percentage") {
      urban[5] = parseInt(value);
    }
  });

  Highcharts.chart("containerpie", {
    chart: {
      type: "variablepie",
    },
    plotOptions: {
      pie: {
        size: 70,
        dataLabels: {
          enabled: true,
          color: "#000",
          format: "{point.name}",
          distance: -25,
          style: {
            fontSize: "20px",
            textOutline: 0,
          },
        },
      },
    },
    colors: ["#E24C4C", "#F740A9", "#0091F7"],
    title: {
      text: "In Urban",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    tooltip: {
      headerFormat: "",
      pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>'
    },
    series: [
      {
        minPointSize: 10,
        innerSize: "20%",
        zMin: 0,
        name: "",
        data: [
          {
            name: "Mixed<br/ ># " + urban[4] + " <br/ > % " + urban[5],
            y: urban[4],
            z: urban[5],

          },
          {
            name: "Girls<br/ ># " + urban[2] + " <br/ > % " + urban[3],
            y: urban[2],
            z: urban[3],
          },
          {
            name: "Boys<br/ ># " + urban[0] + " <br/ > % " + urban[1],
            y: urban[0],
            z: urban[1],
          },
        ],
      },
    ],
  });
}

function locationGenderWisePieChartRural(data) {
  var rural = Array(10).fill(0);
  $.each(data[0], function (key, value) {
    if (key == "Rural_Boys") {
      rural[0] = value;
    } else if (key == "Rural_Boys_percentage") {
      rural[1] = value;
    } else if (key == "Rural_Girls") {
      rural[2] = value;
    } else if (key == "Rural_Girls_percentage") {
      rural[3] = value;
    } else if (key == "Rural_Mixed") {
      rural[4] = value;
    } else if (key == "Rural_Mixed_percentage") {
      rural[5] = value;
    }
  });
  Highcharts.chart("containerpie2", {
    chart: {
      type: "variablepie",
    },
    plotOptions: {
      pie: {
        size: 70,
      },
    },
    colors: ["#FFC415", "#F740A9", "#0091F7"],
    title: {
      text: "In Rural",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    tooltip: {
      headerFormat: "",
      pointFormat:
        '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>',
    },

    series: [
      {
        minPointSize: 10,
        innerSize: "20%",
        zMin: 0,
        name: "gender",
        data: [
          {
            name: "Mixed<br/ ># " + rural[4] + " <br/ > % " + rural[5],
            y: rural[4],
            z: rural[5],
          },
          {
            name: "Girls<br/ ># " + rural[2] + " <br/ > % " + rural[3],
            y: rural[2],
            z: rural[3],
          },
          {
            name: "Boys<br/ ># " + rural[0] + " <br/ > % " + rural[1],
            y: rural[0],
            z: rural[1],
          },
        ],
      },
    ],
  });
}

function enrollmentChart(data, year) {
  var boys;
  var girls;
  var classes;

  if (year == "2021-22") {
    boys = Array(14).fill(0);
    girls = Array(14).fill(0);
    classes = [
      "ECCE",
      "Katchi",
      "Class I",
      "Class II",
      "Class III",
      "Class IV",
      "Class V",
      "Class VI",
      "Class VII",
      "Class VIII",
      "Class IX",
      "Class X",
      "Class XI",
      "Class XII",
    ]
    for (i = 0; i < data.length; i++) {
      $.each(data[i], function (key, value) {
        if (key == "order" && value == 0) {
          boys[0] = data[i]['boys'];
          girls[0] = data[i]['girls'];
        }
        if (key == "order" && value == 1) {
          boys[1] = data[i]['boys'];
          girls[1] = data[i]['girls'];
        } else if (key == "order" && value == 2) {
          boys[2] = data[i]['boys'];
          girls[2] = data[i]['girls'];
        } else if (key == "order" && value == 3) {
          boys[3] = data[i]['boys'];
          girls[3] = data[i]['girls'];
        } else if (key == "order" && value == 4) {
          boys[4] = data[i]['boys'];
          girls[4] = data[i]['girls'];
        } else if (key == "order" && value == 5) {
          boys[5] = data[i]['boys'];
          girls[5] = data[i]['girls'];
        } else if (key == "order" && value == 6) {
          boys[6] = data[i]['boys'];
          girls[6] = data[i]['girls'];
        } else if (key == "order" && value == 7) {
          boys[7] = data[i]['boys'];
          girls[7] = data[i]['girls'];
        } else if (key == "order" && value == 8) {
          boys[8] = data[i]['boys'];
          girls[8] = data[i]['girls'];
        } else if (key == "order" && value == 9) {
          boys[9] = data[i]['boys'];
          girls[9] = data[i]['girls'];
        } else if (key == "order" && value == 10) {
          boys[10] = data[i]['boys'];
          girls[10] = data[i]['girls'];
        } else if (key == "order" && value == 11) {
          boys[11] = data[i]['boys'];
          girls[11] = data[i]['girls'];
        } else if (key == "order" && value == 12) {
          boys[12] = data[i]['boys'];
          girls[12] = data[i]['girls'];
        } else if (key == "order" && value == 13) {
          boys[13] = data[i]['boys'];
          girls[13] = data[i]['girls'];
        }
      });
    }
  } else {
    boys = Array(13).fill(0);
    girls = Array(13).fill(0);
    classes = [
      "Katchi",
      "Class I",
      "Class II",
      "Class III",
      "Class IV",
      "Class V",
      "Class VI",
      "Class VII",
      "Class VIII",
      "Class IX",
      "Class X",
      "Class XI",
      "Class XII",
    ]
    for (i = 0; i < data.length; i++) {
      $.each(data[i], function (key, value) {
        if (key == "order" && value == 1) {
          boys[0] = data[i]['boys'];
          girls[0] = data[i]['girls'];
        }
        if (key == "order" && value == 2) {
          boys[1] = data[i]['boys'];
          girls[1] = data[i]['girls'];
        } else if (key == "order" && value == 3) {
          boys[2] = data[i]['boys'];
          girls[2] = data[i]['girls'];
        } else if (key == "order" && value == 4) {
          boys[3] = data[i]['boys'];
          girls[3] = data[i]['girls'];
        } else if (key == "order" && value == 5) {
          boys[4] = data[i]['boys'];
          girls[4] = data[i]['girls'];
        } else if (key == "order" && value == 6) {
          boys[5] = data[i]['boys'];
          girls[5] = data[i]['girls'];
        } else if (key == "order" && value == 7) {
          boys[6] = data[i]['boys'];
          girls[6] = data[i]['girls'];
        } else if (key == "order" && value == 8) {
          boys[7] = data[i]['boys'];
          girls[7] = data[i]['girls'];
        } else if (key == "order" && value == 9) {
          boys[8] = data[i]['boys'];
          girls[8] = data[i]['girls'];
        } else if (key == "order" && value == 10) {
          boys[9] = data[i]['boys'];
          girls[9] = data[i]['girls'];
        } else if (key == "order" && value == 11) {
          boys[10] = data[i]['boys'];
          girls[10] = data[i]['girls'];
        } else if (key == "order" && value == 12) {
          boys[11] = data[i]['boys'];
          girls[11] = data[i]['girls'];
        } else if (key == "order" && value == 13) {
          boys[12] = data[i]['boys'];
          girls[12] = data[i]['girls'];
        }
      });
    }
  }
  Highcharts.chart("containergender", {
    chart: {
      type: "bar",
    },
    colors: ["#0091F7", "#F740A9"],
    title: {
      text: "Class and Gender wise Enrollments",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },

    xAxis: {
      categories: [
        "Kachi",
        "Class I",
        "Class II",
        "Class II",
        "Class IV",
        "Class V",
        "Class VI",
        "Class VII",
        "Class VIII",
        "Class IX",
        "Class X",
        "Class XI",
        "Class XII",
      ],
      title: {
        text: null,
      },
    },
    yAxis: {
      min: 0,
      title: {
        text: "",
        align: "high",
      },
      labels: {
        overflow: "justify",
      },
    },
    tooltip: {
      valueSuffix: "",
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
          allowOverlap: true,
          crop: false,
          padding: 0,
        },
      },
    },
    legend: {
      layout: "vertical",
      align: "right",
      verticalAlign: "top",
      x: -20,
      y: -10,
      floating: true,
      borderWidth: 1,
      backgroundColor:
        Highcharts.defaultOptions.legend.backgroundColor || "#FFFFFF",
      shadow: true,
    },
    credits: {
      enabled: false,
    },
    series: [
      {
        name: "Boys",
        data: boys,
      },
      {
        name: "Girls",
        data: girls,
      },
    ],
  });
}

function teacherDesigGenderChart(data) {
  var male = Array(10).fill(0)
  var female = Array(10).fill(0)
  $.each(data[0], function (key, value) {
    if (key == "Female_DT") {
      female[0] = value;
    } else if (key == "Female_ECT") {
      female[1] = value;
    } else if (key == "Female_HM") {
      female[2] = value;
    } else if (key == "Female_HST") {
      female[3] = value;
    } else if (key == "Female_JST/JEST") {
      female[4] = value;
    } else if (key == "Female_Non-Government") {
      female[5] = value;
    } else if (key == "Female_Other") {
      female[6] = value;
    } else if (key == "Female_PST") {
      female[7] = value;
    } else if (key == "Female_PTI") {
      female[8] = value;
    } else if (key == "Female_SST") {
      female[9] = value;
    } else if (key == "Female_WIT") {
      female[10] = value;
    }
  });
  $.each(data[0], function (key, value) {
    if (key == "Male_DT") {
      male[0] = value;
    } else if (key == "Male_ECT") {
      male[1] = value;
    } else if (key == "Male_HM") {
      male[2] = value;
    } else if (key == "Male_HST") {
      male[3] = value;
    } else if (key == "Male_JST/JEST") {
      male[4] = value;
    } else if (key == "Male_Non-Government") {
      male[5] = value;
    } else if (key == "Male_Other") {
      male[6] = value;
    } else if (key == "Male_PST") {
      male[7] = value;
    } else if (key == "Male_PTI") {
      male[8] = value;
    } else if (key == "Male_SST") {
      male[9] = value;
    } else if (key == "Male_WIT") {
      male[10] = value;
    }
  });
  Highcharts.chart("containerteacher", {
    chart: {
      type: "bar",
    },
    colors: ["#FFC107", "#0D6EFD"],
    title: {
      text: "Designation and Gender wise Teachers",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },

    xAxis: {
      categories: [
        "Drawing Teacher",
        "Early Childhood Teacher",
        "Head Master / Mistress",
        "High School Teacher",
        "Junior Elementary School Teacher",
        "Non-Government Teacher",
        "Others",
        "Primary School Teacher",
        "Physical Training Instructor",
        "Secondary School Teacher",
        "Workshop Instructor Teacher",
      ],
      title: {
        text: null,
      },
    },
    yAxis: {
      min: 0,
      title: {
        text: "",
        align: "high",
      },
      labels: {
        overflow: "justify",
      },
    },
    tooltip: {
      valueSuffix: "",
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
        },
      },
    },
    legend: {
      layout: "vertical",
      align: "right",
      verticalAlign: "top",
      x: -40,
      y: 80,
      floating: true,
      borderWidth: 1,
      backgroundColor:
        Highcharts.defaultOptions.legend.backgroundColor || "#FFFFFF",
      shadow: true,
    },
    credits: {
      enabled: false,
    },
    series: [
      {
        name: "Female Teacher",
        data: female,
      },
      {
        name: "Male Teacher",
        data: male,
      },
    ],
  });
}

function piefunc(data) {
  // Make monochrome colors
  var pieColors = (function () {
    var colors = ["#008140", "#F70000"],
      base = Highcharts.getOptions().colors[0],
      i;

    for (i = 0; i < 10; i += 1) {
      // Start out with a darkened base color (negative brighten), and end
      // up with a much brighter color
      colors.push(
        Highcharts.color(base)
          .brighten((i - 3) / 7)
          .get()
      );
    }
    return colors;
  })();
  var fun, non_fun;
  $.each(data[0], function (key, value) {
    if (key == "functional_percentage") {
      fun = value;
    } else if (key == "non_functional_percentage") {
      non_fun = value;
    }
  });


  // Build the chart
  Highcharts.chart("containerpiefunc", {
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: "pie",
    },
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    title: {
      text: "",
    },
    tooltip: {
      pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
    },
    accessibility: {
      point: {
        valueSuffix: "%",
      },
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: "pointer",
        colors: pieColors,
        dataLabels: {
          enabled: true,
          format: "<b>{point.name}</b><br>{point.percentage:.1f} %",
          distance: -50,
          filter: {
            property: "percentage",
            operator: ">",
            value: 4,
          },
        },
        showInLegend: false,
      },
    },
    series: [
      {

        name: "",
        data: [
          { name: "Functional", y: data.functional_percentage },
          { name: "Non-functional", y: data.non_functional_percentage },
        ],
      },
    ],
  });
}
