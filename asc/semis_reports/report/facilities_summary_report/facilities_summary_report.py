# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_column()
	data = get_data(filters)
	return columns, data

def get_column():
	column =[
	{
		"label": _("Division"),
		"fieldtype": "Data",
		"fieldname": "division",
		"width": 170
	},
	{
        "label": _("District"),
        "fieldtype": "Data",
        "fieldname": "district",
        "options": "District",
        "width": 150
    },	
	{
		"label": _("Drinking Water"),
        "fieldtype": "String",
        "fieldname": "drinking_water",
        "width": 140
	},
	{
		"label": _("Toilets"),
        "fieldtype": "String",
        "fieldname": "toilets",
        "width": 140
	},
	{
		"label": _("Electricity"),
        "fieldtype": "String",
        "fieldname": "electricity",
        "width": 140
	},
	{
		"label": _("Boundary Wall"),
        "fieldtype": "String",
        "fieldname": "boundary_wall",
        "width": 140
	},
	{
		"label": _("Hand Wash"),
        "fieldtype": "String",
        "fieldname": "hand_wash",
        "width": 140
	},
	{
		"label": _("Total Schools"),
        "fieldtype": "Stringsss",
        "fieldname": "total",
        "width": 140
	},
	]
	return column

def get_data(filters):
	conditions, group_by = get_condition(filters)
    
	temp_query = "SELECT region,district , SUM(if(water_available = 'No' OR water_available IS NULL , 0, 1)), SUM(if( toilet_facility='No' OR toilet_facility='' OR toilet_facility IS NULL, 0, 1) ),	SUM(if(electricity_connection = 'No Electricity Connection' OR electricity_connection='' OR electricity_connection IS NULL,0,1)), SUM(if(condition_of_boundary_wall='No Boundary Wall' OR condition_of_boundary_wall='' OR condition_of_boundary_wall IS NULL, 0, 1) ), SUM(if(hand_wash_facility='No' OR hand_wash_facility='' OR hand_wash_facility IS NULL, 0, 1) ) , count(name) FROM tabASC  WHERE docstatus != 2 %s %s " % (
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