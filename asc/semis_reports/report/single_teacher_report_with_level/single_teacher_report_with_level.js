// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
status_options = ["", "Functional", "Closed"];
frappe.query_reports["Single Teacher Report with Level"] = {
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
      ],
};
