// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
gender_options =["","Boys","Girls","Mixed"]
status_options = ["", "Functional", "Closed"];
level_list = ["", "Primary", "Middle", "Elementary", "Secondary", "Higher Secondary"]
frappe.query_reports["Classroom Summary"] = {
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
			"fieldname": "district",
			"label": __("District"),
			"fieldtype": "Link",
			"options": "District",
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
			fieldname: "level",
			label: __("Level"),
			fieldtype: "Select",
			options: level_list,
		},
		{
			fieldname: "gender",
			label: __("Gender"),
			fieldtype: "Select",
			options: gender_options,
		  },
	]
};
