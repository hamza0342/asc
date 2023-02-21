// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
status_options = ["", "Functional", "Closed"];
school_type = ["", "Sindhi", "Urdu", "English", "Mixed"];
indicators_list = ["", "School", "Male Enrollment", "Female Enrollment", "Total Enrollment", "Male Staff", "Female Staff", "Total Staff", "Male Teaching Staff", "Female Teaching Staff", "Total Teaching Staff", "Male Non-Teaching Staff", "Female Non-Teaching Staff", "Total Non-Teaching Staff"];
building_condition = ["", "Satisfactory", "Needs Repair", "Dangerous"]
electricity_connection = ["", "WAPDA/KE", "Solar System", "No Electricity Connection"]
group_list = ["", "Region", "District", "Taluka", "Level"]
gender_list = ["", "Boys", "Girls", "Mixed"]
level_list = ["", "Primary", "Middle", "Elementary", "Secondary", "Higher Secondary"]
columns_list = ["", "Year wise Analysis", "School Level", "School Gender", "School Type", "School Status"]

frappe.query_reports["Indicators Trend Analysis"] = {
  filters: [
    // {
    //   fieldname: "test_html1",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "<a>INDICATOR:</a>",
    // },
    { 
      fieldname: "indicators_list",
      label: __("Indicator"),
      fieldtype: "Select",
      options: indicators_list,
      default: "School",
      reqd: 1,
    },
    // {
    //   fieldname: "",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "Group by:",
    // },
    {
      fieldname: "group_list",
      label: __("Group By"),
      fieldtype: "Select",
      options: group_list,
      default: "Region",
      reqd: 1,
    },
    // {
    //   fieldname: "",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "Columns:",
    // },
    {
      fieldname: "columns_list",
      label: __("Columns"),
      fieldtype: "Select",
      options: columns_list,
      default: "Year wise Analysis",
      reqd: 1,
      on_change: () => {
        var column_filter = frappe.query_report.get_filter_value('columns_list');
        if (column_filter == "School Level" || column_filter == "School Status" || column_filter == "School Type" || column_filter == "School Gender") {
          var year_filter = frappe.query_report.get_filter("year")
          year_filter.df.hidden = 0;
          year_filter.df.reqd = 1;
          frappe.query_report.set_filter_value("year", "");
          year_filter.refresh();

        } else {
          var year_filter = frappe.query_report.get_filter("year")
          // console.log(year_filter);

          year_filter.df.hidden = 1;
          year_filter.df.reqd = 0;
          frappe.query_report.set_filter_value("year", "");
          year_filter.refresh();
          // console.log(year_filter);

        }
      },

    },
    {
      fieldname: "year",
      label: __("Year"),
      fieldtype: "Link",
      options: "Year",
      hidden: 1,
      // reqd: 1,
    },
    // {
    //   fieldname: "test_html",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "Location Filter:",
    // },
    {
      fieldname: "division",
      label: __("Division"),
      fieldtype: "Link",
      options: "Division",
    },
    {
      fieldname: "district",
      label: __("District"),
      fieldtype: "Link",
      options: "District",
    },
    // {
    //   fieldname: "",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "School Category Filters:",
    // },
    {
      fieldname: "level",
      label: __("Level"),
      fieldtype: "Select",
      options: level_list,
    },
    {
      fieldname: "school_gender",
      label: __("Gender"),
      fieldtype: "Select",
      options: gender_list,
    },
    {
      fieldname: "school_type",
      label: __("School Type"),
      fieldtype: "Select",
      options: school_type,
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: status_options,
    },
    {
      fieldname: "location",
      label: __("Location"),
      fieldtype: "Select",
      options: loc_options,
    },
    // {
    //   fieldname: "",
    //   label: "Indicator List",
    //   fieldtype: "HTML",
    //   options: "Facilities Filters:",
    // },
    {
      fieldname: "building_availability",
      label: __("Building Availability"),
      fieldtype: "Select",
      options: ["", "Yes", "No"],
    },
    {
      fieldname: "condition_of_building",
      label: __("Building Condition"),
      fieldtype: "Select",
      options: building_condition,
    },
    {
      fieldname: "electricity_connection",
      label: __("Electricity Connection"),
      fieldtype: "Select",
      options: electricity_connection,
    },
    {
      fieldname: "water_available",
      label: __("Water Available"),
      fieldtype: "Select",
      options: ["", "Yes", "No"],
    }
  ]
};
