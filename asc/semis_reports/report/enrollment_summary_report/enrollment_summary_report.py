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
		"label":_("District"),
		"fieldtype":"link",
		"fieldname":"district",
		"options":"District",
		"width": 150
		},{
		"label":_("Male Enrollment"),
		"fieldtype":"Int",
		"fieldname":"male_enrollment",
		"width": 150
		},{
			"label":_("Female Enrollment"),
			"fieldtype":"Int",
			"fieldname":"female_enrollment",
			"width": 150
		},{
			"label":_("TotalEnrollment"),
			"fieldtype":"Int",
			"fieldname":"total_enrollment",
			"width": 150
		},{
			"label":_("Student / Teacher"),
			"fieldtype":"Int",
			"fieldname":"str",
			"width": 150
		}]
	return columns
def get_data(filters):
	conditions= get_condition(filters)
	query="""(SELECT t.district,SUM(male_enrollment),
	SUM(female_enrollment) ,
	SUM(total_enrollment) ,
	IFNULL( SUM( IFNULL(total_enrollment,0)) / SUM( IFNULL(total_teacher,0)) ,0)
	FROM tabASC t
	WHERE t.docstatus != 2  %s
	GROUP BY  t.district)
	UNION ALL
	(SELECT "Total",SUM(male_enrollment),
	SUM(female_enrollment) ,
	SUM(total_enrollment) ,
	IFNULL( SUM( IFNULL(total_enrollment,0)) / SUM( IFNULL(total_teacher,0)) ,0)
	FROM tabASC t
	WHERE t.docstatus != 2  %s )
	""" % (conditions,conditions)
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
