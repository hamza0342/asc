frappe.pages['district-profile-test'].on_page_load = async function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'Provincial Dashboard',
    single_column: true
  });

  filters.add(page);
  wrapper.page.add_inner_button(__('Print'), () => {
    window.print()
  });


  $(frappe.render_template("test_skeleton")).appendTo(page.main);


  frappe.call({
    method: "asc.dashboards.page.district_profile_test.district_profile_test.get_role",
    args: {
      year: "2021-22",
    },
    callback: function (r) {
      $('#side_bar_').empty();
      $(frappe.render_template("side_bar", { "user_roles": r.message })).appendTo("#side_bar_");
    },
  });

  await frappe.call({
    method: "asc.dashboards.page.district_profile_test.district_profile_test.get_data",
    args: {
      year: "2021-22",
    },
    callback: function (r) {
      console.log(r.message);

      $('#provincial_dashboard').empty();
      $(frappe.render_template("body_data", r.message[0])).appendTo("#provincial_dashboard");

      $("#year_hidden").val(r.message[0].year);

      $('#girls_prog').css('width', r.message[0].girls_percentage + '%')
      $('#boys_prog').css('width', r.message[0].boys_percentage + '%')
      $('#mixed_prog').css('width', r.message[0].mixed_percentage + '%')
    },

  });

  frappe.call({
    method: "asc.dashboards.page.district_profile_test.district_profile_test.get_chart_data",
    args: {
      year: "2021-22",
    },
    callback: function (r) {
      genderLevelGraph(r.message);
    },
  });

};

var genderLevelGraph_data;

filters = {
  add: function (page) {
    let year = page.add_field({
      label: "Year",
      fieldtype: "Link",
      fieldname: "Year",
      options: "Year",
      default: "2021-22",
      reqd: 1,
    });
    let fiterbtn = page.add_field({
      label: "View",
      fieldtype: "Button",
      fieldname: "filter",
      async click() {
        if (year.get_value() == "") {
          frappe.msgprint("Please Select Year")
          return;
        }

        $('#side_bar').remove();


        $(frappe.render_template("test_skeleton")).appendTo(page.main);


        frappe.call({
          method: "asc.dashboards.page.district_profile_test.district_profile_test.get_role",
          args: {
            year: year.get_value(),
          },
          callback: function (r) {
            $('#side_bar_').empty();
            $(frappe.render_template("side_bar", { "user_roles": r.message })).appendTo("#side_bar_");
          },
        });

        await frappe.call({
          method: "asc.dashboards.page.district_profile_test.district_profile_test.get_data",
          args: {
            year: year.get_value(),
          },
          callback: function (r) {
            console.log(r.message);

            $('#provincial_dashboard').empty();
            $(frappe.render_template("body_data", r.message[0])).appendTo("#provincial_dashboard");

            $("#year_hidden").val(r.message[0].year);

            $('#girls_prog').css('width', r.message[0].girls_percentage + '%')
            $('#boys_prog').css('width', r.message[0].boys_percentage + '%')
            $('#mixed_prog').css('width', r.message[0].mixed_percentage + '%')
          },

        });

        frappe.call({
          method: "asc.dashboards.page.district_profile_test.district_profile_test.get_chart_data",
          args: {
            year: year.get_value(),
          },
          callback: function (r) {
            genderLevelGraph(r.message);
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
      type: "column",
      height: 380,
    },
    colors: ["#454d66", "#0091F7", "#F740A9"],
    credits: {
      enabled: false,
    },
    exporting: {
      enabled: false,
    },
    title: {
      text: "",

    },
    xAxis: {
      categories: [
        "Primary",
        "Middle",
        "Elementary",
        "Secondary",
        "Higher Secondary",
      ],
      "labels": {

        style: {
          fontSize: '12px',
          fontWeight: '500'
        }

      },
    },
    yAxis: {
      min: 0,
      title: {
        text: "",
      },
    },

    legend: {
      reversed: true,
      align: "center",


    },
    plotOptions: {

      series: {
        pointWidth: 60,
        groupPadding: 0,
        stacking: "percent",
        dataLabels: {
          style: {
            fontSize: '14px',
          },
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

function open_gender_wise_report() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "Gender Wise Summary", { "year": year });
}

function open_functional_wise_report() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "Functional and Non Functional Schools by District and Level", { "year": year });
}
function open_closed_school_reports() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "Closed Schools Summary", { "year": year });
}

function open_shift_wise_report() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "Shift wise school Summary", { "year": year });
}

function open_enrollment_reports() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "Enrollment Summary Report", { "year": year });
}

function open_teachers_reports() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "School Staff Summary with Districts", { "year": year });
}

function open_building_reports() {
  var year = $("#year_hidden").val()
  frappe.set_route("query-report", "School Building Report", { "year": year });
}

function open_drinking_water() {
  frappe.ui.toolbar.clear_cache()
  var year = $("#year_hidden").val()
  frappe.set_route("facilities-map", year, "Drinking Water");
}
function open_electricity() {
  frappe.ui.toolbar.clear_cache()
  var year = $("#year_hidden").val()
  frappe.set_route("facilities-map", year, "Electricity");
}

function open_toilet() {
  frappe.ui.toolbar.clear_cache()
  var year = $("#year_hidden").val()
  frappe.set_route("facilities-map", year, "Toilet");
}

function open_hand_wash() {
  frappe.ui.toolbar.clear_cache()
  var year = $("#year_hidden").val()
  frappe.set_route("facilities-map", year, "Hand Wash");
}

function open_boundary_wall() {
  frappe.ui.toolbar.clear_cache()
  var year = $("#year_hidden").val()
  frappe.set_route("facilities-map", year, "Boundary Wall");
}