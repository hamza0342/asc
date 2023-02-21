// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Status of Facilities"] = {
	"filters": [
		{
			"fieldname":"level",
			"label": __("School Level"),
			"fieldtype": "Link",
			"options": "Level",
		},
		{
			"fieldname":"school_gender",
			"label": __("School Gender"),
			"fieldtype": "Link",
			"options": "School Gender",
		},
		{
			"fieldname":"data_type",
			"label": __("Data Type"),
			"fieldtype": "Select",
			"options": ["Number", "Percentage"],
			"default": 'Number'
		}
	],
};
