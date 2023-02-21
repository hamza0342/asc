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
		"label": _("Level"),
		"fieldtype": "Link",
		"fieldname": "level",
		"options": "Level",
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

	temp_query = """SELECT tabLevel.name , 
 	SUM(physical_disabilites + polio_affected), 
  	SUM(physical_disabilites),	SUM(polio_affected), 
   	SUM(CASE WHEN wheel_chair_ramp_available = 'Yes' Then 1 Else 0 END) FROM tabASC CROSS JOIN tabLevel ON tabASC.level = tabLevel.name  
    WHERE tabASC.docstatus != 2 %s %s ORDER BY tabLevel.list_order asc""" % (
			conditions, group_by)

	info = frappe.db.sql(temp_query, filters)

	return info

def get_condition(filters):
	conditions , group_by = "" , "GROUP BY tabLevel.name"

	if filters.get("division"):
		conditions += " AND region = %(division)s"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("district"):
		conditions += " AND district = %(district)s"
	if filters.get("gender"):
		conditions += " AND school_gender = %(gender)s"

	return conditions, group_by
    