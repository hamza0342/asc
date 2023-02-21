# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    get_gender = ["Boys", "Girls", "Mixed"]
    get_status = ["Functional","Closed"]
    colmn = get_columns(get_gender, get_status)
    columns = colmn[0]
    #frappe.msgprint(len(colmn))
    data = get_data(filters, colmn[1])
   
    return columns, data


def get_columns(gender, status):
    columns = []
    columns.append(
        {
            "label": _("Level"),
            "fieldtype": "Link",
            "fieldname": "level",
            "options": "Level",
            "width": 150
        }
    )
    case_string = ""
    for gndr in gender:
        for sts in status:
            
            columns.append(
                {
                    "label": _("") + str(gndr) + "-" + str(sts),
                    "fieldtype": "Int",
                    "fieldname": str(gndr).lower() + "-" + str(sts).lower(),
                    "width": 140
                }
            )

            case_string += "Sum( Case WHEN  status_detail = '%s' and  school_gender= '%s' THEN 1 ELSE 0 END)," % (
                str(sts), str(gndr))
    
    
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
    temp_query = "SELECT  tabLevel.name , %s  count( tabASC.name) FROM tabASC Cross JOIN tabLevel ON tabASC.level=tabLevel.name  WHERE tabASC.docstatus != 2 %s %s ORDER BY tabLevel.list_order " % (
        str(case_string), conditions, group_by)
    info = frappe.db.sql(temp_query, filters)
    return info


def get_condition(filters):
    conditions, group_by = "", "GROUP BY  tabLevel.name"
    if filters.get("division"):
        conditions += " AND  region = %(division)s"
    if filters.get("year"):
        conditions += "  AND  year = %(year)s"
    if filters.get("location"):
        conditions += "  AND  location = %(location)s"
    if filters.get("district"):
        conditions += "  AND  district = %(district)s"
    return conditions, group_by
