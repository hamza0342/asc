# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	columns = get_columns(filters)
	conditions, filters = get_conditions(filters)
	data = get_data(conditions, filters)
	return columns, data

def get_data(conditions, filters):
	performance = frappe.db.sql("""SELECT 
									`tabASC`.owner, 
									u.full_name, 
									u.district,
									COUNT(`tabASC`.owner)
									FROM `tabASC`  inner join `tabUser` u 
									on `tabASC`.owner = u.name 
									WHERE `tabASC`.docstatus = 1 and `tabASC`.owner != 'Administrator'  %s 
									group by `tabASC`.owner"""% conditions, filters)
	return performance

def get_conditions(filters):
	conditions=""
	if filters.get("district"):
		conditions = "  and `tabASC`.district = %(district)s"
	return conditions, filters

def get_columns(filters):
	columns = [
		_("User ID") + "::120",
		_("User Name") + "::120",
		_("District") + ":Link/District:120",
		_("Created ASC") + "::120",
		]
	# columns.append({
    #         "label": _("District"),
    #         "fieldtype": "Link",
    #         "fieldname": "district",
    #         "options": "District",
    #         "width": 150
    # })
	return columns