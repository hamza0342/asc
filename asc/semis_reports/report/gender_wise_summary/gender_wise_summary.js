// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
// console.log("route", frappe.get_route());

var default_year = "2021-22";

if (frappe.get_route()[2]) {
	default_year = frappe.get_route()[2]
}
console.log("defaul............", default_year);
frappe.query_reports["Gender Wise Summary"] = {


	"filters": [
		{
			"fieldname": "year",
			"label": __("Year"),
			"fieldtype": "Link",
			"options": "Year",
			"default": default_year,
			"reqd": 1
		},
		{
			"fieldname": "division",
			"label": __("Division"),
			"fieldtype": "Link",
			"options": "Division",
		}
	]
};
