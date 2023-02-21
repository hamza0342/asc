# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	get_level = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
	get_gender = frappe.db.get_list('School Gender', pluck='name', order_by='name desc')
	columnss = get_columns(get_level, get_gender)
	columns = columnss[0]
	data = get_employees(filters,columnss[1])
	return columns, data


def get_columns(get_level, get_gender):
	columns =  []
	columns.append(
            {
                "label": _("Division"),
                "fieldtype": "Data",
                "fieldname": "division",
                "width": 170
            }
        )
	columns.append({
		"label": _("District"),
		"fieldtype": "Data",
		"fieldname": "district",
		"options": "District",
		"width": 150
	})
	case_string = ""
	for lvl in get_level:
		for gen in get_gender:
			columns.append({
			"label": _("") + str(lvl) +"-"+ str(gen),
			"fieldtype": "Int",
			"fieldname": str(lvl).lower() +"-"+ str(gen).lower(),
			"width": 140
			})
			case_string += " SUM(CASE WHEN census.school_gender = '%s' and census.level = '%s' THEN 1 ELSE 0 END), " % (str(gen), str(lvl))
	columns.append({
		"label": _("Total"),
		"fieldtype": "Int",
		"fieldname": "total",
		"width": 150
	})	
	return columns, case_string

def get_employees(filters, case_string):
	conditions, group_by = get_conditions(filters)
	tem_query = "SELECT census.region,census.district, %s count(census.name) FROM tabASC census WHERE census.docstatus != 2 %s %s" %(str(case_string), conditions, group_by)
	info = frappe.db.sql(tem_query, filters)
	return info
	
def get_conditions(filters):
	conditions , group_by = "", "GROUP BY census.region,census.district Order By census.region,census.district"
	if filters.get("division"):
		conditions += "  and census.region = %(division)s"
		group_by = "GROUP BY census.region, census.district Order By census.region,census.district "
	if filters.get("year"):
		conditions += "  and census.year = %(year)s"
	return conditions, group_by
