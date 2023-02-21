# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [{
        "label": _("District"),
        "fieldtype": "Data",
        "fieldname": "district",
        "width": 150
    },
        {
        "label": _("Govt. Male Teachers"),
        "fieldtype": "Int",
        "fieldname": "govt_male_teachers",
        "width": 150
    },
        {
        "label": _("Govt. Female Teachers"),
        "fieldtype": "Int",
        "fieldname": "govt_female_teachers",
        "width": 150
    },
        {
        "label": _("Non-Govt. Male Teachers"),
        "fieldtype": "Int",
        "fieldname": "non_govt_male_teachers",
        "width": 150
    },
        {
        "label": _("Non-Govt. Female Teachers"),
        "fieldtype": "Int",
        "fieldname": "non_govt_female_teachers",
        "width": 150
    },
        {
        "label": _("Total Teachers"),
        "fieldtype": "Int",
        "fieldname": "total_teachers",
        "width": 150
    },
        {
        "label": _("Total Non-Teaching Staff"),
        "fieldtype": "Int",
        "fieldname": "total_non_teacher_staff",
        "width": 150
    }
    ]
    return columns


def get_data(filters):
    conditions = get_conditiions(filters)
    temp_query = """Select district, SUM(govt_male_teachers), SUM(govt_female_teachers), 
	SUM(non_govt_male_teachers), SUM(non_govt_female_teachers), 
	SUM(govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers),
	SUM(non_teaching_male_staff + non_teaching_female_staff + IFNULL(non_teaching_non_government_male_staff,0)+IFNULL(non_teaching_non_government_female_staff,0)) 
	from tabASC where docstatus!=2 %s GROUP BY district""" % (conditions)
    data = frappe.db.sql(temp_query, filters)
    return data


def get_conditiions(filters):
    conditions = ""
    if filters.get("division"):
        conditions += " AND  region = %(division)s"
        # group_by = "GROUP BY  t.region,  district"
    if filters.get("year"):
        conditions += "  AND  year = %(year)s"
    if filters.get("location"):
        conditions += "  AND  location = %(location)s"
    if filters.get("status"):
        conditions += "  AND  status_detail = %(status)s"
    if filters.get("district"):
        conditions += " AND district = %(district)s"
    return conditions
