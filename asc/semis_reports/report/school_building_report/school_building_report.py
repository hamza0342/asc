# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
from pkgutil import get_data
import frappe
from frappe import _
def execute(filters=None):
	columns, data = [], []
	columns,hut_string=get_columns(filters)
	data=get_data(filters,hut_string)
	return columns, data

def get_columns(filters):
	hut_string = ''
	columns=[
		{
		"label":_("District"),
		"fieldtype":"link",
		"fieldname":"district",
		"options":"District",
		"width": 150
		},{
		"label":_("Total Schools"),
		"fieldtype":"Int",
		"fieldname":"number_of_school",
		"width": 150
		},{
			"label":_("Have Building Schools"),
			"fieldtype":"Int",
			"fieldname":"building_of_school",
			"width": 210
		},{
			"label":_("Government Building Schools"),
			"fieldtype":"Int",
			"fieldname":"gov_building_of_school",
			"width": 250
		},{
			"label":_("Non-Government Building Schools"),
			"fieldtype":"Int",
			"fieldname":"other_of_school",
			"width": 250
		},{
			"label":_("No Building Schools"),
			"fieldtype":"Int",
			"fieldname":"not_have_building_of_school",
			"width": 160
		},{
			"label":_("Tree Schools"),
			"fieldtype":"Int",
			"fieldname":"tree_school",
			"width": 150
		},{
			"label":_("Chappra Schools"),
			"fieldtype":"Int",
			"fieldname":"chappra_school",
			"width": 150
		}]
	if filters.get("year") != '2021-22':
		columns.append(
			{
			"label":_("Hut School"),
			"fieldtype":"Int",
			"fieldname":"hut_school",
			"width": 150
		}
		)
		hut_string = ',	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Hut"THEN 1 ELSE 0 END) hut'
	return columns, hut_string
def get_data(filters,hut_string):
	conditions= get_condition(filters)
	query="""SELECT t.district,count(name),
	SUM(CASE WHEN t.availability_of_building="Yes" THEN 1 ELSE 0 END) as building,
	SUM(CASE WHEN t.yes_relevant_code="Government Building" THEN 1 ELSE 0 END) g_Building,
	SUM(CASE WHEN  t.availability_of_building="Yes" and t.yes_relevant_code!="Government Building" THEN 1 ELSE 0 END) another_building,
	SUM(CASE WHEN t.availability_of_building="No" THEN 1 ELSE 0 END) no_building,
	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Tree" THEN 1 ELSE 0 END) tree,
	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Chappra"THEN 1 ELSE 0 END) chupra %s
	FROM tabASC t
	WHERE t.docstatus != 2  %s
	GROUP BY  t.district""" % (hut_string,conditions)
	info = frappe.db.sql(query, filters)
	return info





def get_condition(filters):
	conditions = ""
	if filters.get("division"):
		conditions += " AND  t.region = %(division)s"
		# group_by = "GROUP BY  t.region,  district"
	if filters.get("year"):
		conditions += "  AND  t.year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  t.location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  t.status_detail = %(status)s"
	if filters.get("level"):
		conditions += " AND t.level = %(level)s"
	return conditions
