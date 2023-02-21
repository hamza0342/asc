// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
status_options = ["", "Functional", "Closed"]
gender_options =["","Boys","Girls","Mixed"]
frappe.query_reports["KPI Level Wise Summary"] = {
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
			"fieldname": "division",
			"label": __("Division"),
			"fieldtype": "Link",
			"options": "Division",
		},
		  {
			"fieldname": "district",
			"label": __("District"),
			"fieldtype": "Link",
			"options": "District",
		},
		{
			"fieldname": "taluka",
			"label": __("Taluka"),
			"fieldtype": "Link",
			"options": "Taluka",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: status_options,
			// default: "Functional",
		  },
		  {
			fieldname: "gender",
			label: __("Gender"),
			fieldtype: "Select",
			options: gender_options,
		  },
	]
};
function open_report(Division, Year,District,Tehsil,Status) {
	// console.log(Division)
	// console.log(Year)
	// console.log(District)
	// console.log(Status)

	if(Year && Status){
		frappe.query_report.set_filter_value("year", Year);
		frappe.query_report.set_filter_value("status", Status);
	}
	if (Division && Year){
	frappe.query_report.set_filter_value("division", Division);
	frappe.query_report.set_filter_value("status", Status);
	}
	if (Division && Year && Status){
		frappe.query_report.set_filter_value("division", Division);
	}
	if (Division && Year && District){
		frappe.query_report.set_filter_value("district", District);
	}
	if (Division && Year && District && Tehsil){
		frappe.query_report.set_filter_value("taluka", Tehsil);
		frappe.set_route("query-report", "School List Export", {"Division": Division,"District": District,"Tehsil": Tehsil, "Year": Year});
	}
	// if (Division && Year && District && Tehsil && Status){
	// 	frappe.query_report.set_filter_value("taluka", Tehsil);
	// 	frappe.set_route("query-report", "School List Export", {"Division": Division,"District": District,"Tehsil": Tehsil, "Year": Year,"Status":Status});
	// }
	}