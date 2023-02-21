// Copyright (c) 2022, Micromerger and contributors
// For license information, please see license.txt
/* eslint-disable */
indiciators_list = ["", "School", "Male Enrollment", "Female Enrollment", "Total Enrollment"]
group_list = ["", "Region", "District","Taluka", "Level"]
columns_list = ["", "Year wise analysis", "School Level", "School Gender", "School Type", "School Status"]

frappe.query_reports["Practice"] = {
	filters: [
		// {
		// 	fieldname: "test_html1",
		// 	label: "Indicator list",
		// 	fieldtype: "HTML",
		// 	options: "Indicator"
		// },
		{
			fieldname: "indicators_list",
			label: __("Indicator"),
			fieldtype: "Select",
			options: indiciators_list,
			default: "School",
			reqd: 1,
		},
		{
			fieldname: "group_list",
			label: __("Group By"),
			fieldtype: "Select",
			options: group_list,
			default: "Region",
			reqd:1,

		},
		{
			fieldname:"columns_list",
			label: __("Column"),
			fieldtype:"Select",
			options: columns_list,
			default: "Year wise analysis",
			reqd:1,
			on_change: () => {
				var column_filter = frappe.query_report.get_filter_value('columns_list');
				if (column_filter == "School Level" || column_filter == "School Status" || column_filter == "School Type" || column_filter == "School Gender") {
				  var year_filter = frappe.query_report.get_filter("year")
				  year_filter.df.hidden = 0;
				  year_filter.df.reqd = 1;
				  frappe.query_report.set_filter_value("year", "");
				  year_filter.refresh();
		
				} else {
				  var year_filter = frappe.query_report.get_filter("year")
				  //console.log(year_filter);
		
				  year_filter.df.hidden = 1;
				  year_filter.df.reqd = 0;
				  frappe.query_report.set_filter_value("year", "");
				  year_filter.refresh();
				  //console.log(year_filter);
		
				}
			  },
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Link",
			options: "Year",
			hidden: 1,
			// reqd: 1,
		  }
	]
};
   