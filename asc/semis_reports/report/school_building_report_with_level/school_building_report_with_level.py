# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
from pkgutil import get_data
import frappe
from frappe import _
def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters)
	return columns, data

def get_columns():
    columns=[
		{
		"label":_("Level"),
		"fieldtype":"link",
		"fieldname":"level",
		"options":"Level",
		"width": 150
		},{
		"label":_("Total School"),
		"fieldtype":"Int",
		"fieldname":"number_of_school",
		"width": 150
		},{
			"label":_("School having Building"),
			"fieldtype":"Int",
			"fieldname":"building_of_school",
			"width": 180
		},{
			"label":_("Government Building School"),
			"fieldtype":"Int",
			"fieldname":"gov_building_of_school",
			"width": 170
		},{
			"label":_("Non Government Building School"),
			"fieldtype":"Int",
			"fieldname":"other_of_school",
			"width": 150
		},{
			"label":_("No Building School"),
			"fieldtype":"Int",
			"fieldname":"not_have_building_of_school",
			"width": 150
		},{
			"label":_("Tree's School"),
			"fieldtype":"Int",
			"fieldname":"tree_school",
			"width": 150
		},{
			"label":_("Chappra School"),
			"fieldtype":"Int",
			"fieldname":"chappra_school",
			"width": 150
		},{
			"label":_("Hut School"),
			"fieldtype":"Int",
			"fieldname":"hut_school",
			"width": 150
		}]
    return columns
def get_data(filters):
	conditions= get_condition(filters)
	query="""SELECT t.level,count(t.name), 
	SUM(CASE WHEN t.availability_of_building="Yes" THEN 1 ELSE 0 END) as building,
	SUM(CASE WHEN  t.yes_relevant_code="Government Building" THEN 1 ELSE 0 END) g_Building,
	SUM(CASE WHEN  t.availability_of_building="Yes" and t.yes_relevant_code!="Government Building" THEN 1 ELSE 0 END) another_building,
	SUM(CASE WHEN t.availability_of_building="No" THEN 1 ELSE 0 END) no_building,
	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Tree" THEN 1 ELSE 0 END) tree,
	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Chappra"THEN 1 ELSE 0 END) chupra,
	SUM(CASE WHEN t.availability_of_building="No" AND t.no_relevant_code="Hut"THEN 1 ELSE 0 END) hut
	FROM tabASC t Left JOIN tabLevel ON t.level=tabLevel.name  
	WHERE t.docstatus != 2  %s
	GROUP BY  t.level ORDER BY tabLevel.list_order""" % (conditions)
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
	if filters.get("school_gender"):
		conditions += " AND t.school_gender = %(school_gender)s"
	return conditions
