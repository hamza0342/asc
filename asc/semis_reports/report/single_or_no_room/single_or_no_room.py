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
		"label": _("District"),
		"fieldtype": "Link",
		"fieldname": "district",
		"options": "District",
		"width": 150
	},
	{
		"label": _("Total Schools"),
		"fieldtype": "Int",
		"fieldname": "total",
		"width": 140
	},
	{
		"label": _("Single Room"),
		"fieldtype": "Int",
		"fieldname": "single_room",
		"width": 140
	},
	{
		"label": _("No Room"),
		"fieldtype": "Int",
		"fieldname": "no_room",
		"width": 140
	}
	]
	return columns

def get_data(filters):
	conditions, group_by = get_condition(filters)
	temp_query= "SELECT district, count(name) , SUM(CASE WHEN total_rooms = 1 THEN 1 ELSE 0 END),SUM(CASE WHEN total_rooms = 0 THEN 1 ELSE 0 END) FROM tabASC  WHERE docstatus != 2 %s %s ORDER BY district" % (conditions, group_by)
	info = frappe.db.sql(temp_query, filters)
	return info

def get_condition(filters):
	conditions , group_by = "" , "GROUP BY district"
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
