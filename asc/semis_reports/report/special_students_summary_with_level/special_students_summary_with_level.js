// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

let loc_options = ["", "Urban", "Rural"];
let status_options = ["", "Functional", "Closed"];
let gender_options = ["", "Boys", "Girls", "Mixed"];
frappe.query_reports["Special Students Summary With Level"] = {
  filters: [
    {
      fieldname: "year",
      label: __("Year"),
      fieldtype: "Link",
      options: "Year",
      default: "2021-22",
			reqd: 1
    },
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
      "get_query": function() {
			var division = frappe.query_report.get_filter_value('division');
			if (division) {
			  return {
				"doctype": "District",
				"filters": {
				  "division": division,
				}
			  }
			}
		  }
    },
    {
      fieldname: "location",
      label: __("Location"),
      fieldtype: "Select",
      options: loc_options,
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: status_options,
    },
    {
      fieldname: "gender",
      label: __("Gender"),
      fieldtype: "Select",
      options: gender_options,
    },
  ],
};
