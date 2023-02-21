# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[
     {
		"label": _("District"),
		"fieldtype": "Data",
		"fieldname": "district",
		"width": 150
	},
     {
		"label": _("Total Schools"),
		"fieldtype": "Int",
		"fieldname": "total_schools",
		"width": 145
	},
    {
		"label": _("Schools by Web"),
		"fieldtype": "Int",
		"fieldname": "schools_by_web",
		"width": 170
	},
    {
		"label": _("Schools by Mobile"),
		"fieldtype": "Int",
		"fieldname": "schools_by_mobile",
		"width": 180
	},
    {
		"label": _("Total Visited"),
		"fieldtype": "Int",
		"fieldname": "total_visited",
		"width": 150
	},
    {
		"label": _("Remaining Schools"),
		"fieldtype": "Int",
		"fieldname": "remaining_schools",
		"width": 175
	},
    {
		"label": _("Total Images"),
		"fieldtype": "Int",
		"fieldname": "total_images",
		"width": 180
	}
	]
	return columns

def get_data(filters):
	tem_query = """SELECT s.district as "District", 
	sum(s.Schools) as "Total Schools",
	sum(i.web) as "Schools by Web",
	sum(i.mobile) as "School by Mobile",
	sum(i.total) as "Total Visited",
	sum(s.Schools)-sum(i.total) as "Remaining Schools",
	sum(i.totalimages) as "Total Images"
	FROM
	(SELECT district, count(name) as Schools FROM tabSchool WHERE enabled = '1' GROUP BY district) s
	LEFT JOIN 
	(SELECT district,COUNT(DISTINCT CASE WHEN source = 'Web' THEN semis_code END) as web,
	COUNT(DISTINCT CASE WHEN source = 'Mobile' THEN semis_code END) as mobile,
	count(name) as total,
	sum(total_images) as totalimages
	FROM `tabASC Images` where enabled=1 GROUP BY district ) i ON s.district = i.district
	GROUP by s.district ORDER BY sum(i.total)""" 
	info = frappe.db.sql(tem_query, filters)
	return info


