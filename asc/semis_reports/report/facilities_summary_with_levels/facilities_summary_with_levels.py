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
        "label": _("Level"),
        "fieldtype": "Link",
        "fieldname": "level",
        "options": "Level",
        "width": 150
    },	
	{
		"label": _("Drinking Water"),
        "fieldtype": "Int",
        "fieldname": "drinking_water",
        "width": 140
	},
	{
		"label": _("Toilets"),
        "fieldtype": "Int",
        "fieldname": "toilets",
        "width": 140
	},
	{
		"label": _("Electricity"),
        "fieldtype": "Int",
        "fieldname": "electricity",
        "width": 140
	},
	{
		"label": _("Boundary Wall"),
        "fieldtype": "Int",
        "fieldname": "boundary_wall",
        "width": 140
	},
	{
		"label": _("Hand Wash"),
        "fieldtype": "Int",
        "fieldname": "hand_wash",
        "width": 140
	},
	{
		"label": _("Total Schools"),
        "fieldtype": "Int",
        "fieldname": "total",
        "width": 140
	},
	]
	return column

def get_data(filters):
	conditions, group_by = get_condition(filters)
    
	temp_query = """SELECT tabLevel.name , 
 	SUM(if(water_available = 'No' OR water_available IS NULL , 0, 1)), 
  	SUM(if( toilet_facility='No' OR toilet_facility='' OR toilet_facility IS NULL, 0, 1) ),
   	SUM(if(electricity_connection = 'No Electricity Connection' OR electricity_connection='' OR electricity_connection IS NULL,0,1)),
    SUM(if(condition_of_boundary_wall='No Boundary Wall' OR condition_of_boundary_wall='' OR condition_of_boundary_wall IS NULL, 0, 1) ),
    SUM(if(hand_wash_facility='No' OR hand_wash_facility='' OR hand_wash_facility IS NULL, 0, 1) ) , count(tabASC.name)
    FROM tabASC CROSS JOIN tabLevel ON tabASC.level = tabLevel.name   
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
    
	return conditions, group_by