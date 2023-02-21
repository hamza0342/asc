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
	columns =[
	{
		"label": _("District"),
		"fieldtype": "Link",
		"fieldname": "district",
		"options": "District",
		"width": 150
	},
	{
		"label": _("Total"),
		"fieldtype": "Int",
		"fieldname": "total",
		"width": 150
	},
	{
		"label": _("Main"),
		"fieldtype": "Int",
		"fieldname": "main",
		"width": 150
	},
	{
		"label": _("Branch"),
		"fieldtype": "Int",
		"fieldname": "branch",
		"width": 150
	},
	{
		"label": _("Adopted"),
		"fieldtype": "Int",
		"fieldname": "adopted",
		"width": 150
	},
	{
		"label": _("Campus"),
		"fieldtype": "Int",
		"fieldname": "campus",
		"width": 150
	},
	{
		"label": _("Merged"),
		"fieldtype": "Int",
		"fieldname": "merged",
		"width": 150
	}
	]
	return columns

def get_data(filters):
	conditions, group_by = get_condition(filters)
	temp_query = """SELECT district,count(name),
	sum(case when is_this_branch_school="Main" then 1 else 0 end ), 
	sum(case when is_this_branch_school="Branch" then 1 else 0 end ) 
	,SUM(case when adopted_school ="Yes" then 1 else 0 end)  ,SUM(case when is_campus_school ="Yes" then 1 else 0 end),
	SUM(no_of_merger_schools)
	from tabASC  WHERE docstatus != 2 %s %s ORDER BY district""" % (
			conditions, group_by)

	info = frappe.db.sql(temp_query, filters)

	return info


def get_condition(filters):
	conditions , group_by = "" , "GROUP BY region,district Order By region,district"

	if filters.get("division"):
		conditions += " AND region = %(division)s"
		group_by = " GROUP BY region, district Order By region,district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("level"):
		conditions += " AND level = %(level)s"

	return conditions, group_by
    