# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	get_gen = ["Boys","Girls","Mixed"]
	get_loc = ["Urban","Rural"]
	colmn = get_columns(get_gen,get_loc,filters)
	columns = colmn[0]
	#frappe.msgprint(len(colmn))
	data = get_data(filters, colmn[1])

	return columns, data

def get_columns(gen, loc,filters):
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
	if filters.get("location")=="Rural":
		loc=["Rural"]
	elif filters.get("location")=="Urban":
		loc=["Urban"]
	
	for lc in loc:
		for gn in gen:
			
			columns.append(
				{
					"label": _("") +  str(lc) + "-" +str(gn),
					"fieldtype": "Int",
					"fieldname":  str(lc).lower() + "-" +str(gn).lower(),
					"width": 140
				}
			)

			case_string += "Sum( Case WHEN  location = '%s' and gender= '%s' THEN 1 ELSE 0 END)," % (
				str(lc), str(gn))
	
	
	columns.append(
				{
					"label": _("Total"),
					"fieldtype": "Int",
					"fieldname": "total",
					"width": 150
				}
			)
		

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
	if filters.get("level"):
		conditions += "  AND  level = %(level)s"
	if filters.get("status"):
		conditions += "  AND  status = %(status)s"
	if filters.get("shift"):
		conditions += "  AND  shift = %(shift)s"
	if filters.get("gender"):
		conditions += "  AND  gender = %(gender)s"
	return conditions, group_by