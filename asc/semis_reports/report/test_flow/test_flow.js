// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Test Flow"] = {
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
			"fieldname": "district",
			"label": __("District"),
			"fieldtype": "Link",
			"options": "District",
			// "hidden": 1
		}
	]
};
function open_report(District, Year) {
	console.log(District)
	console.log(Year)
	frappe.query_report.set_filter_value("district", District);
	}