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
	amount_disbursed = frappe.db.sql("""SELECT region,district,
count(name) as total_school,
SUM(CASE WHEN smc_received_detail='Yes' THEN 1 ELSe 0 end) as school_recived,
SUM(t_r_smc) as amount_recived
FROM `tabASC`
WHERE 1 %s
Group By region,district
ORDER BY region,district ASC"""% conditions, filters)
	return amount_disbursed

def get_conditions(filters):
	conditions=""
	if filters.get("year"):
		conditions += "  AND  Year = %(year)s"
	if filters.get("level1"):
		conditions = "  and level = %(level1)s"
	if filters.get("gender"):
		conditions += "  and school_gender = %(gender)s"
	if filters.get("location"):
		conditions += "  and location = %(location)s"
	return conditions, filters

def get_columns(filters):
	columns = [
		_("Division") + "::240",
		_("District") + "::240",
		_("Total School") + "::220",
		_("No of School Recived") + "::220",
		_("Amount received") + ":Currency:230"
		]
		
	return columns
