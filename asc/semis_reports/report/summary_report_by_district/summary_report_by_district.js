// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
let loc_options = ["", "Urban", "Rural"];
let status_options = ["", "Functional", "Closed"];
let shift_options = ["", "Morning", "Afternoon", "Both"];
let gender_options = ["", "Boys", "Girls", "Mixed"];
frappe.query_reports["Summary Report by District"] = {
  filters: [
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
      fieldname: "shift",
      label: __("Shift"),
      fieldtype: "Select",
      options: shift_options,
    },
    {
      fieldname: "gender",
      label: __("Gender"),
      fieldtype: "Select",
      options: gender_options,
    },
  ],
};
