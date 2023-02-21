# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
		"label": _("Division"),
        "fieldtype": "Data",
        "fieldname": "division",
        "width": 170
		},

		{
		"label": _("District"),
		"fieldtype": "Link",
		"fieldname": "district",
		"options": "District",
		"width": 150
	},
	{
		"label": _("Total Disables"),
		"fieldtype": "Int",
		"fieldname": "total_disables",
		"width": 150
	},
	{
		"label": _("Physical Disables"),
		"fieldtype": "Int",
		"fieldname": "physical_disables",
		"width": 150
	},
	{
		"label": _("Polio Affected"),
		"fieldtype": "Int",
		"fieldname": "polio_affected",
		"width": 150
	},
	{
		"label": _("Wheel Chair Ramps"),
		"fieldtype": "Int",
		"fieldname": "wheel_chair_ramps",
		"width": 150
	},
	]
	return columns

def get_data(filters):
	conditions, group_by = get_condition(filters)

	temp_query = "SELECT region,district , SUM(physical_disabilites + polio_affected), SUM(physical_disabilites),	SUM(polio_affected), SUM(CASE WHEN wheel_chair_ramp_available = 'Yes' Then 1 Else 0 END)FROM tabASC  WHERE docstatus != 2 %s %s ORDER BY district" % (
			conditions, group_by)

	info = frappe.db.sql(temp_query, filters)

	return info

def get_condition(filters):
	conditions , group_by = "" , "GROUP BY region,district"

	if filters.get("division"):
		conditions += " AND region = %(division)s"
		group_by = " GROUP BY region, district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("level"):
		conditions += " AND level = %(level)s"

	return conditions, group_by
    