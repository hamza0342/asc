# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns(filters)
	school_data = get_school_data()
	# print(filters.get("level"))
	# filters.get("level")
	
	
	return columns, school_data

def get_school_data():
	schools = frappe.db.sql("""select 
							s.school_name,s.taluka,s.union_council,s.school_type,s.level,
							(select count(name) from `tabASC` where docstatus=1 and district=s.district)
							from `tabSchool` s
							group by s.district""")
	return schools
# WHERE docstatus=1 and docstatus=2 as_dict=1
def get_columns(filters):
	columns = [
		_("School Name") + "::130",		
		_("Taluka") + "::180",
		_("Union Council") + "::180",
		_("Type") + "::180",
		_("Level") + "::180",
		_("Completed") + "::180",

	]
	return columns