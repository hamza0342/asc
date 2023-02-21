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
	if filters.get("data_type") =='Percentage':
		electricity = frappe.db.sql("""select 
							district,
							sum(case when (district=district) then 1 else 0 end) as total,
							round(sum(case when (district=district and hand_wash_facility ='No') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end), 1) as no_total,
							round(sum(case when (district=district and hand_wash_facility ='Yes') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end), 1) as yes_total
							from `tabASC`
							where district=district %s
							group by district """% conditions, filters)
	else:
		electricity = frappe.db.sql("""select 
							district,
							sum(case when (district=district) then 1 else 0 end) as total,
							sum(case when (district=district and hand_wash_facility ='No') then 1 else 0 end) as no_total,
							sum(case when (district=district and hand_wash_facility ='Yes') then 1 else 0 end) as yes_total
							from `tabASC`
							where district=district %s
							group by district """% conditions, filters)
	
	return electricity

def get_conditions(filters):
	conditions=""
	if filters.get("level"):
		conditions = "  and level = %(level)s"
	if filters.get("school_gender"):
		conditions = "  and school_gender = %(school_gender)s"
	if filters.get("level") and filters.get("school_gender"):
		conditions = "  and level = %(level)s and school_gender = %(school_gender)s"
	
	return conditions, filters

def get_columns(filters):
	columns = [
		_("District") + "::120",
		_("Total School") + "::120",
		_("Not Available") + "::110",
		_("Available") + "::100",
		]
		
	return columns
