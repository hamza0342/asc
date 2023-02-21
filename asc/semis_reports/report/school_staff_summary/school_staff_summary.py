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
		"label":_("District"),
		"fieldtype":"link",
		"fieldname":"district",
		"options":"District",
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
		"label":_("Male-Enrolment"),
		"fieldtype":"Int",
		"fieldname":"male_Enrolment", 
		"width": 150
	},{
		"label":_("Female-Enrolment"),
		"fieldtype":"Int",
		"fieldname":"female_Enrolment", 
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
	query="""SELECT t.district,
	count( (t.name)),
	IFNULL(SUM(t.total_teacher),0),
	SUM(IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)),
	IFNULL(SUM(s.boys),0),
	IFNULL(SUM(s.girls),0),
	IFNULL(SUM(t.total_rooms),0)
	FROM `tabASC` t 
	Inner JOIN (Select tabASC.name , SUM(e.boys) as boys,SUM(e.girls) as girls from tabASC Left join `tabEnrolment Class and Gender wise` e ON tabASC.name=e.parent where tabASC.docstatus !=2 %s group by tabASC.name ) s
	ON t.name=s.name Where t.docstatus != 2 %s
    group BY t.district""" % (conditions,conditions)
	info = frappe.db.sql(query, filters)
	return info

def get_condition(filters):
	conditions = ""
	if filters.get("division"):
		conditions += " AND  region = %(division)s"
		# group_by = "GROUP BY  t.region,  district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("level"):
		conditions += " AND level = %(level)s"
	return conditions