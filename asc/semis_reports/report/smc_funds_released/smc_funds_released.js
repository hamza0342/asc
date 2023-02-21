// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
gender_options = ["", "Boys", "Girls", "Mixed"]
frappe.query_reports["SMC Funds Released"] = {
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
			fieldname: "gender",
			label: __("Gender"),
			fieldtype: "Select",
			options: gender_options,
		},
		{
			fieldname: "location",
			label: __("Location"),
			fieldtype: "Select",
			options: ["", "Urban", "Rural"],
		}
	]
};
