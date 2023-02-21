// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["ASC Images Summary"] = {
	"filters": [ 
		{
			fieldname: "year", 
			label: __("Year"),
			fieldtype: "Data",
			default : "2021-22",
			read_only: 1,

		},
	]
};

