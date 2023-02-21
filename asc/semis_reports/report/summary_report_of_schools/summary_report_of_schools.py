# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	school_gender = ["Boys","Girls","Mixed"]
	colmn = get_columns(school_gender,filters)
	columns = colmn[0]
	data = get_data(filters , colmn[1])
	return columns, data

def get_columns(gender,filters):
	columns = []
	columns.append({
		"label": _("Level"),
		"fieldtype": "Link",
		"fieldname": "level",
		"options": "Level",
		"width": 150}
	)
	case_string_scl=""
	if filters.get("gender")=="Boys":
		gender=["Boys"]
	elif filters.get("gender")=="Girls":
		gender=["Girls"]
	elif filters.get("gender")=="Mixed":
		gender=["Mixed"]
	for gndr in gender:
		columns.append(
			{
					"label": _("") + str(gndr) + " Schools" ,
					"fieldtype": "Int",
					"fieldname": str(gndr).lower() + "_schools" ,
					"width": 140
				}
		)
		case_string_scl += " Count( DISTINCT   CASE WHEN tabSchool.gender = '%s' THEN tabSchool.name ELSE NULL END), " %(str(gndr))
	columns.append(  
					{
					"label": _("Total Schools") ,
					"fieldtype": "Int",
					"fieldname": "Total Schools" ,
					"width": 140
				}
					)

	return columns, case_string_scl
    
def get_data(filters , case_string):
	conditions , group_by = get_condition(filters)
	
	temp_query= """Select tabLevel.name , %s COUNT(DISTINCT tabSchool.name)
				FROM tabSchool 
				CROSS JOIN tabLevel ON tabSchool.level = tabLevel.name  
				WHERE (tabSchool.docstatus != 2 ) %s %s ORDER BY tabLevel.list_order asc"""% (
			str(case_string), conditions, group_by)
	info = frappe.db.sql(temp_query,filters)
	return info

def get_condition(filters):
	conditions, group_by = "", "GROUP BY  tabLevel.name"
	if filters.get("division"):
		conditions += " AND  division = %(division)s"
	if filters.get("district"):
		conditions += "  AND  district = %(district)s"
	if filters.get("taluka"):
		conditions += "  AND  taluka = %(taluka)s"
	if filters.get("union_council"):
		conditions += "  AND  union_council = %(union_council)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status = %(status)s"
	if filters.get("shift"):
		conditions += "  AND  shift = %(shift)s"
	return conditions, group_by