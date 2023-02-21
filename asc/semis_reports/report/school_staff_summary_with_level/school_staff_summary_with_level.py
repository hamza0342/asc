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
	columns=[{
		"label":_("Level"),
		"fieldtype":"link",
		"fieldname":"level",
		"options":"Level",
		"width": 150
	},{
		"label":_("Number of School"),
		"fieldtype":"Int",
		"fieldname":"number_of_school",
		"width": 150
	},{
		"label":_("Teaching Staff"),
		"fieldtype":"Int",
		"fieldname":"teaching_staff", 
		"width": 150
	},{
		"label":_("Non-Teaching Staff"),
		"fieldtype":"Int",
		"fieldname":"non_teaching_staff",
		"width": 150
	},{
		"label":_("Male-Student"),
		"fieldtype":"Int",
		"fieldname":"male_Student", 
		"width": 150
	},{
		"label":_("Female-Student"),
		"fieldtype":"Int",
		"fieldname":"female_Student", 
		"width": 150
	},{
		"label":_("Class rooms"),
		"fieldtype":"Int",
		"fieldname":"class_rooms", 
		"width": 150
	}]
	return columns
	
def get_data(filters):
	conditions= get_condition(filters)
	query="""SELECT t.level,
	count(DISTINCT (t.name)),
	SUM(t.total_teacher),
	SUM(t.total_non_teaching_staff),
	IFNULL(SUM(e.boys),0),
	IFNULL(SUM(e.girls),0),
	SUM(t.total_rooms)
	FROM `tabASC` t 
	CROSS JOIN tabLevel ON t.level=tabLevel.name
	LEFT JOIN `tabEnrolment Class and Gender wise` e 
	ON t.name=e.parent and t.docstatus != 2 and e.docstatus != 2 %s
	GROUP BY  t.level ORDER BY tabLevel.list_order asc""" % (conditions)

	temp_query = """SELECT t.level,
	count( (t.name)),
	IFNULL(SUM(t.total_teacher),0),
	SUM(IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)),
	IFNULL(SUM(s.boys),0),
	IFNULL(SUM(s.girls),0),
	IFNULL(SUM(t.total_rooms),0)
	FROM `tabASC` t 
	Inner JOIN (Select t.name , SUM(e.boys) as boys,SUM(e.girls) as girls from tabASC t Left join `tabEnrolment Class and Gender wise` e ON t.name=e.parent where t.docstatus !=2 %s group by t.name ) s
	ON t.name=s.name CROSS JOIN 
    tabLevel on t.level = tabLevel.name Where t.docstatus != 2 %s
    group BY t.level order by tabLevel.list_order"""%(conditions,conditions)
	info = frappe.db.sql(temp_query, filters)
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
	if filters.get("district"):
		conditions += " AND t.district = %(district)s"
	return conditions