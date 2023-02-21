# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
from pkgutil import get_data
import frappe
from frappe import _
def execute(filters=None):
	columns, data = [], []
	columns,case_string=get_columns(filters)
	data=get_data(filters,case_string)
	return columns, data

def get_columns(filters):
	columns = []
	columns.append({
		"label":_("District"),
		"fieldtype":"link",
		"fieldname":"district",
		"options":"District",
		"width": 150
		}
		)
	case_string=""
	year = filters.get("year")
	closed_reasons = frappe.db.sql("Select DISTINCT major_reason_closure from tabASC where year = '%s' and major_reason_closure != '' "%(year))
	for c in closed_reasons:
		columns.append({
		"label":_(c),
		"fieldtype":"Int",
		"fieldname":c[0],
		"width": 200
		}
		)
		case_string += ", SUM(CASE WHEN major_reason_closure = '%s' Then 1 ELSE 0 END) "%(c)

	return columns,case_string

def get_data(filters,case_string):
	conditions= get_condition(filters)
	query="""SELECT t.district %s
	FROM tabASC t
	WHERE t.docstatus != 2  %s  GROUP BY  t.district Order By  t.district
	""" % (case_string,conditions)
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
	if filters.get("level"):
		conditions += " AND t.level = %(level)s"
	return conditions
