# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    get_level = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
    colmn = get_columns(get_level)
    columns = colmn[0]
    #frappe.msgprint(len(colmn))
    data = get_data(filters, colmn[1])
   
    return columns, data


def get_columns(level):
	columns = []
	columns.append(
		{
			"label": _("District"),
			"fieldtype": "Link",
			"fieldname": "district",
			"options": "District",
			"width": 150
		}
	)
	case_string = ""
	for lvl in level:
			columns.append({
							"label": _("") + str(lvl) ,
							"fieldtype": "Int",
							"fieldname": str(lvl).lower() ,
							"width": 140
						})
			case_string += "Sum( Case WHEN level= '%s' THEN 1 ELSE 0 END)," % (
				str(lvl))
	
	
	columns.append(
				{
					"label": _("Total"),
					"fieldtype": "Int",
					"fieldname": "total",
					"width": 150
				}
			)
			# frappe.msgprint(case_string)

	return columns, case_string


def get_data(filters, case_string):
    conditions, group_by = get_condition(filters)
    temp_query = "SELECT  district , %s  count( name) FROM tabSchool  WHERE docstatus != 2 %s %s" % (
        str(case_string), conditions, group_by)
    info = frappe.db.sql(temp_query, filters)
    return info


def get_condition(filters):
	conditions, group_by = "", "GROUP BY  district"
	#if filters.get("year"):
	#	conditions += "  AND  year = %(year)s"
	if filters.get("division"):
		conditions += " AND  division = %(division)s"
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
	if filters.get("gender"):
		conditions += "  AND  gender = %(gender)s"
	return conditions, group_by