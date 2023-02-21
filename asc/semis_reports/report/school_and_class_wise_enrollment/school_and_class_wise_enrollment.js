// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["School and Class wise Enrollment"] = {
	"filters": [
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
			"get_query": function () {
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
			fieldname: "taluka",
			label: __("Taluka"),
			fieldtype: "Link",
			options: "Taluka",
			"get_query": function () {
				var district = frappe.query_report.get_filter_value('district');
				if (district) {
					return {
						"doctype": "Taluka",
						"filters": {
							"district": district,
						}
					}
				}
			}
		},

		{
			fieldname: "level",
			label: __("Level"),
			fieldtype: "Link",
			options: "Level",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Functional", "Closed"],
		},
	]
};
