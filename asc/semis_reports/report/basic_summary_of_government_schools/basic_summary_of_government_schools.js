// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Basic Summary of Government Schools"] = {
	"filters": [
		{
			"fieldname": "level",
			"label": __("Level"),
			"fieldtype": "Select",
			"options": "Primary\nMiddle\nSecondary\nHigher Secondary",
			"default": ["Primary", "Middle", "Secondary", "Higher Secondary",
				"Dec"
			]
			// [frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth()],
		}
	],
	// "filters": [
	// 	{
	// 		"fieldname":"date",
	// 		"label": __("Date"),
	// 		"fieldtype": "Date",
	// 		"default": frappe.datetime.get_today(),
	// 		"reqd": 1
	// 	}
	// ]
	// "onload": function() {
	// 	return frappe.call({
	// 		method: "frappe.rsu.report.basic_summary_of_government_schools.basic_summary_of_government_schools.get_attendance_years",
	// 		// callback: function(r) {
	// 		// 	var year_filter = frappe.query_report.get_filter('year');
	// 		// 	year_filter.df.options = r.message;
	// 		// 	year_filter.df.default = r.message.split("\n")[0];
	// 		// 	year_filter.refresh();
	// 		// 	year_filter.set_input(year_filter.df.default);
	// 		// }
	// 	});
	// }

};
