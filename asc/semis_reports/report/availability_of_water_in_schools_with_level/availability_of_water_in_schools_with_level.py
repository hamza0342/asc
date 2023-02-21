# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	get_mode = frappe.db.get_list('Mode of provision of Drinking Water', pluck='name')
	columnss=get_columns(get_mode)
	columns = columnss[0]
	data = get_data(filters,columnss[1])
	return columns, data

def get_columns(mode):
	columns=[]
	columns.append({
		"label": _("Level"),
		"fieldtype": "Link",
		"fieldname": "level",
		"options": "Level",
		"width": 150
	})
	columns.append({
		"label": _("Total Schools"),
		"fieldtype": "Int",
		"fieldname": "school",
		"width": 150
	})
	columns.append({
		"label": _("Water Available"),
		"fieldtype": "Int",
		"fieldname": "available",
		"width": 150
	})
	case_string=""
	for md in mode:
		if md == "No Water":
			continue
		columns.append({
		"label": _("")+"Mode - " + str(md),
		"fieldtype": "Int",
		"fieldname": str(md).lower(),
		"width": 140
		})		
		case_string += " SUM(CASE WHEN t.provision_drinking_water= '%s' THEN 1 ELSE 0 END), " % str(md)
	columns.append({
		"label": _("Water Not Available"),
		"fieldtype": "Int",
		"fieldname": "not_available",
		"width": 150
	})

	return columns,case_string


def get_data(filters, case_string):
	conditions, group_by = get_conditions(filters)
	tem_query = """SELECT t.level,count(t.name),
	sum(CASE WHEN t.water_available = "Yes" then 1 else 0 end), %s 
 	sum(CASE WHEN t.water_available = "No" then 1 else 0 end) 
  	FROM tabASC t Left JOIN tabLevel ON t.level=tabLevel.name  
   	WHERE t.docstatus != 2 
    %s %s 
    ORDER BY tabLevel.list_order""" %(str(case_string), conditions, group_by)
	info = frappe.db.sql(tem_query, filters)
	return info


def get_conditions(filters):
	conditions , group_by = "", "GROUP BY t.level"
	if filters.get("division"):
		conditions += " AND  t.region = %(division)s"
	if filters.get("year"):
		conditions += "  AND  t.year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  t.location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  t.status_detail = %(status)s"
	if filters.get("district"):
		conditions += " AND t.district = %(district)s"
	if filters.get("gender"):
		conditions += " AND school_gender = %(gender)s"
	return conditions,group_by