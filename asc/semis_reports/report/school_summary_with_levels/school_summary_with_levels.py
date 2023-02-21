# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    school_gender = ["Boys","Girls","Mixed"]
    colmn = get_columns(school_gender)
    columns = colmn[0]
    data = get_data(filters , colmn[1])
    return columns, data

def get_columns(gender):
    columns = []
    columns.append({
            "label": _("Level"),
            "fieldtype": "Link",
            "fieldname": "level",
            "options": "Level",
            "width": 150}
    )
    case_string_scl=""
    for gndr in gender:
        columns.append(
                {
                                "label": _("") + str(gndr) + " Schools" ,
                                "fieldtype": "Int",
                                "fieldname": str(gndr).lower() + "_schools" ,
                                "width": 140
                        }
        )
        case_string_scl += " Count( DISTINCT   CASE WHEN tabASC.school_gender = '%s' THEN tabASC.name ELSE NULL END), " %(str(gndr))
    columns.append(  
                                    {
                                        "label": _("Total Schools") ,
                                        "fieldtype": "Int",
                                        "fieldname": "Total Schools" ,
                                        "width": 140
                                    }
                                    )


    columns.append(
                    {
                                    "label": _("Boys Enrollment") ,
                                    "fieldtype": "Int",
                                    "fieldname": "boys_students" ,
                                    "width": 140
                            }
            )

    columns.append(
                    {
                                    "label": _("Girls Enrollment") ,
                                    "fieldtype": "Int",
                                    "fieldname": "girls_students" ,
                                    "width": 140
                            }
            )

    columns.append(  
                                    {
                                        "label": _("Total Enrollment") ,
                                        "fieldtype": "Int",
                                        "fieldname": "Total Students" ,
                                        "width": 140
                                    }
                                    )

    return columns, case_string_scl

def get_data(filters , case_string):
    conditions , group_by = get_condition(filters)

    temp_query= """Select tabASC.level , %s COUNT(DISTINCT tabASC.name), SUM(enrol.boys) , SUM(enrol.girls), SUM(enrol.total_class)
    			FROM tabASC LEFT JOIN `tabEnrolment Class and Gender wise` as enrol ON 
       			tabASC.name = enrol.parent CROSS JOIN tabLevel ON tabASC.level = tabLevel.name WHERE (tabASC.docstatus != 2 ) %s %s ORDER BY tabLevel.list_order asc"""% (
                str(case_string), conditions, group_by)  
    info = frappe.db.sql(temp_query,filters)
    return info

def get_condition(filters):
    conditions, group_by = "", "GROUP BY  tabLevel.name"
    if filters.get("division"):
        conditions += " AND  region = %(division)s"
    if filters.get("year"):
        conditions += "  AND  year = %(year)s"
    if filters.get("location"):
        conditions += "  AND  tabASC.location = %(location)s"
    if filters.get("status"):
        conditions += "  AND  tabASC.status_detail = %(status)s"
    if filters.get("district"):
        conditions += "  AND  tabASC.district = %(district)s"
    return conditions, group_by