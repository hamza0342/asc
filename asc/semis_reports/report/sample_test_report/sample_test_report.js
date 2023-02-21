// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sample test report"] = {
	"filters": [{
		fieldname: "number_filter",
		label: "Number Filter",
		fieldtype: "Select",
		//You can supply the options as a string of new-line (\n) separated values,
		//    or as an array of strings such as options: ["1","2","3","4","5","6","7"],
		options: "1\n2\n3\n4\n5\n6\n7",
		default: 3

	},
	{
		fieldname: "date_filter",
		label: "Date Filter",
		fieldtype: "Date",
		//Note the following default attribute, which contains an API call
		default: frappe.datetime.get_today()
	},
	{
		fieldname: "check_filter",
		label: "Check Filter",
		fieldtype: "Check",
		default: 1,
	},
	{
		fieldname: "user_filter",
		label: "User Filter",
		fieldtype: "Link",
		options: "User",
		reqd: 0,
	}
	]
};
