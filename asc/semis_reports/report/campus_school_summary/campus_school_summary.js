// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
status_options = ["", "Functional", "Closed"];
frappe.query_reports["Campus School Summary"] = {
  filters: [
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
      fieldname: "location",
      label: __("Location"),
      fieldtype: "Select",
      options: loc_options,
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: status_options,
    },
    {
      fieldname: "level",
      label: __("level"),
      fieldtype: "Link",
      options: "Level",
    },
  ],
};
