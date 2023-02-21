frappe.pages["main-dashboard"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Main Dashboard",
    single_column: true,
  });


  $('#loader').remove();
  $('#main_dashboard').remove();
  var img = $('<img />', {
    id: 'loader',
    src: '/assets/img/loading.gif',
    alt: 'Loading',
    style: 'text-align:center; margin:0 auto; display:block'
  });
  img.appendTo(page.main);
  var genderLevelGraph_data;


  frappe.call({
    method: "asc.dashboards.page.main_dashboard.main_dashboard.get_chart_data",
    args: {
      year: "2020-21",
    },
    callback: function (r) {
      genderLevelGraph_data = r.message;
    },
  });
  frappe.call({
    method: "asc.dashboards.page.main_dashboard.main_dashboard.get_data",
    args: {
      year: "2020-21",

    },
    callback: function (r) {
      $('#main_dashboard').remove();
      $('#loader').remove();
      $(frappe.render_template("main_dashboard", r.message[0])).appendTo(
        page.main
      );
      $('#girls_prog').css('width', r.message[0].girls_percentage + '%')
      $('#boys_prog').css('width', r.message[0].boys_percentage + '%')
      $('#mixed_prog').css('width', r.message[0].mixed_percentage + '%')
      genderLevelGraph(genderLevelGraph_data);

    },
  });


  filters.add(page);
};

filters = {
  add: function (page) {
    let year = page.add_field({
      label: "Year",
      fieldtype: "Link",
      fieldname: "Year",
      options: "Year",
      default: "2020-21",
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
          frappe.msgprint("Please Select Filters")
          return;
        }
        $('#loader').remove();
        $('#main_dashboard').remove();
        var img = $('<img />', {
          id: 'loader',
          src: '/assets/img/loading.gif',
          alt: 'Loading',
          style: 'text-align:center; margin:0 auto; display:block'
        });
        img.appendTo(page.main);
        var genderLevelGraph_data;


        frappe.call({
          method: "asc.dashboards.page.main_dashboard.main_dashboard.get_chart_data",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            genderLevelGraph_data = r.message;
          },
        });
        frappe.call({
          method: "asc.dashboards.page.main_dashboard.main_dashboard.get_data",
          args: {
            district: district.get_value(),
            year: year.get_value(),
          },
          callback: function (r) {
            $('#main_dashboard').remove();
            $('#loader').remove();
            $(frappe.render_template("main_dashboard", r.message[0])).appendTo(
              page.main
            );
            $('#girls_prog').css('width', r.message[0].girls_percentage + '%')
            $('#boys_prog').css('width', r.message[0].boys_percentage + '%')
            $('#mixed_prog').css('width', r.message[0].mixed_percentage + '%')
            genderLevelGraph(genderLevelGraph_data);

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
