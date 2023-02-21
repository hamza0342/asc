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
								round(sum(case when (district=district and electricity_connection ='No Electricity Connection') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end), 2) as no_total,
								round(sum(case when (district=district and electricity_connection !='No Electricity Connection') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end),2) as yes_total,
								round(sum(case when (district=district and electricity_connection ='Solar System') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end), 2) as yes_total,
								round(sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Functional') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end),2) as f_total,
								round(sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Partially Functional') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end),2) as pf_total,
								round(sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Non-Functional') then 1 else 0 end)*100/sum(case when (district=district) then 1 else 0 end), 2) as nf_total
								from `tabASC`
								where district=district %s
								group by district """% conditions, filters)
	else:

		electricity = frappe.db.sql("""select 
							district,
							sum(case when (district=district) then 1 else 0 end) as total,
							sum(case when (district=district and electricity_connection ='No Electricity Connection') then 1 else 0 end) as no_total,
							sum(case when (district=district and electricity_connection !='No Electricity Connection') then 1 else 0 end) as yes_total,
							sum(case when (district=district and electricity_connection ='Solar System') then 1 else 0 end) as yes_total,
							sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Functional') then 1 else 0 end) as f_total,
							sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Partially Functional') then 1 else 0 end) as pf_total,
							sum(case when (district=district and electricity_connection ='WAPDA/KE' and status_of_electrification='Non-Functional') then 1 else 0 end) as nf_total
							from `tabASC`
							group by district """)
	
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
		_("District") + "::100",
		_("Total School") + "::80",
		_("Not Available") + "::110",
		_("Available") + "::100",
		_("Solar System") + "::100",
		_("Functional") + "::100",
		_("Partially Functional") + "::150",
		_("Non-Functional") + "::130",
		]
		
	return columns
