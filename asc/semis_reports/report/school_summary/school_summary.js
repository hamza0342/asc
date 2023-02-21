// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
status_options = ["", "Functional", "Closed"]
frappe.query_reports["School Summary"] = {
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
			fieldname: "level1",
			label: __("Level"),
			fieldtype: "Link",
			options: "Level",
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
			options: ["", "Urban", "Rural"],
		}
	]
};
