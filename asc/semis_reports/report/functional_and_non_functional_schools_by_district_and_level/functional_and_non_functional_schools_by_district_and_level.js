// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
loc_options = ["", "Urban", "Rural"];
frappe.query_reports["Functional and Non Functional Schools by District and Level"] = {
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
  ],
};
