// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Gross Enrollment Rate(GER)"] = {
	"filters": [
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
			"options": ["","2018-19","2019-20","2020-21","2021-22"],
			"default": "2021-22",
			"reqd": 1
		}
	]
};
