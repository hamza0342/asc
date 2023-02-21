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
	data=get_data(filters, colmn[1])
	return columns, data

def get_columns(level):
	columns=[]
	columns.append(
            {
                "label": _("Division"),
                "fieldtype": "Data",
                "fieldname": "division",
                "width": 170
            }
        )
	columns.append(
		{
			"label": _("District"),
			"fieldtype": "Data",
			"fieldname": "district",
			"options": "District",
			"width": 150
		}
	)
	columns.append(
		{
			"label": _("Total"),
			"fieldtype": "Int",
			"fieldname": "total",
			"width": 140
		}
	)
	case_string = ""
	for lvl in level:
		columns.append(
			{
					"label": _("") + str(lvl) ,
					"fieldtype": "Int",
					"fieldname": str(lvl).lower() ,
					"width": 140
				}
		)
		case_string += ", SUM( CASE WHEN level = '%s' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END ) " %(str(lvl))
		

	return columns, case_string

def get_data(filters, case_string):
	conditions , group_by = get_condition(filters)
	temp_query = "SELECT tabASC.region,tabASC.district ,   SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment)  %s  FROM tabASC   WHERE tabASC.docstatus != 2  %s  %s" % (
		str(case_string), conditions, group_by)
	info = frappe.db.sql(temp_query, filters)
	return info

def get_condition(filters):
	conditions, group_by = "", "GROUP BY  region,district"
	if filters.get("division"):
		conditions += " AND  region = %(division)s"
		group_by = "GROUP BY  region,  district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	return conditions, group_by