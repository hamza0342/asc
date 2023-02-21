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
            "label": _("District"),
            "fieldtype": "Link",
            "fieldname": "district",
            "options": "District",
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
            "width": 190
    })
    case_string=""
    for md in mode:
        if md == "No Water":
            continue
        columns.append({
            "label": _("")+"Mode - " + str(md),
            "fieldtype": "Int",
            "fieldname": str(md).lower(),
            "width": 170
        })
        case_string += " SUM(CASE WHEN t.provision_drinking_water= '%s' THEN 1 ELSE 0 END), " % str(md)
    columns.append({
            "label": _("Water Not Available"),
            "fieldtype": "Int",
            "fieldname": "not_available",
            "width": 190
    })
    return columns,case_string

def get_data(filters, case_string):
    conditions, group_by = get_conditions(filters)
    tem_query = """SELECT t.district,count(t.name),
	sum(CASE WHEN t.water_available = "Yes" then 1 else 0 end) , %s sum(CASE WHEN t.water_available = "No" then 1 else 0 end) FROM tabASC t  WHERE t.docstatus != 2 %s %s""" %(str(case_string), conditions, group_by)
    info = frappe.db.sql(tem_query, filters)
    return info

def get_conditions(filters):
    conditions , group_by = "", "GROUP BY t.district"
    if filters.get("division"):
        conditions += " AND  t.region = %(division)s"
        group_by = "GROUP BY  t.region,  district"
    if filters.get("year"):
        conditions += "  AND  t.year = %(year)s"
    if filters.get("location"):
        conditions += "  AND  t.location = %(location)s"
    if filters.get("status"):
        conditions += "  AND  t.status_detail = %(status)s"
    if filters.get("level"):
        conditions += " AND t.level = %(level)s"
    return conditions,group_by
