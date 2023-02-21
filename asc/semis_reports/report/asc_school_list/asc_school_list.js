// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
status_options = ["", "Functional", "Closed"];
school_type = ["", "Sindhi", "Urdu", "English", "Mixed"];
building_condition = ["", "Satisfactory", "Needs Repair", "Dangerous"]
electricity_connection = ["", "WAPDA/KE", "Solar System", "No Electricity Connection"]
group_list = ["", "Region", "District", "Taluka", "Level"]
gender_list = ["", "Boys", "Girls", "Mixed"]
level_list = ["", "Primary", "Middle", "Elementary", "Secondary", "Higher Secondary"]
frappe.query_reports["ASC School List"] = {
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
			fieldname: "division",
			label: __("Division"),
			fieldtype: "Link",
			options: "Division",
		},
		{
			fieldname: "district",
			label: __("District"),
			fieldtype: "Link",
			options: "District",
		},
		{
			fieldname: "level",
			label: __("Level"),
			fieldtype: "Select",
			options: level_list,
		},
		{
			fieldname: "school_gender",
			label: __("Gender"),
			fieldtype: "Select",
			options: gender_list,
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: status_options,
		},
		{
			fieldname: "location",
			label: __("Location"),
			fieldtype: "Select",
			options: loc_options,
		},
		
		{
			fieldname: "building_availability",
			label: __("Building Availability"),
			fieldtype: "Select",
			options: ["", "Yes", "No"],
		},
		{
			fieldname: "condition_of_building",
			label: __("Building Condition"),
			fieldtype: "Select",
			options: building_condition,
		},
		{
			fieldname: "electricity_connection",
			label: __("Electricity Connection"),
			fieldtype: "Select",
			options: electricity_connection,
		},
		{
			fieldname: "water_available",
			label: __("Water Available"),
			fieldtype: "Select",
			options: ["", "Yes", "No"],
		}
	]
};
