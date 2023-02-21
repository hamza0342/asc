// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Teaching Staff Detail"] = {
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
			fieldname: "school",
			label: __("School"),
			fieldtype: "Link",
			options: "School",
			reqd: 1,
		},
	]
};
