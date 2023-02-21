 # Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns(filters)
	districtdata_data = get_level_wise()
	# print(filters.get("level"))
	# filters.get("level")
	
	
	return columns, districtdata_data

def get_level_wise():
	schools = frappe.db.sql("""select sch.level,
							(select count(level) from `tabSchool` where location='Urban' and level=sch.level) as urban,
							(select count(level) from `tabSchool` where location='Rural' and level=sch.level) as rular,
							count(sch.level) as total,
							round(((select count(level) from `tabSchool` where location='Urban' and level=sch.level)/(select count(level) from `tabSchool`)*100),2) as UrbanAvg,
							round(((select count(level) from `tabSchool` where location='Rural' and level=sch.level)/(select count(level) from `tabSchool`)*100),2) as RuralAvg,
							round((count(sch.level)/(select count(level) from `tabSchool`)*100),2) as TotalAvg
							from `tabSchool` as sch group by sch.level""")

	return schools
# WHERE docstatus=1 and docstatus=2 as_dict=1
#  count(a.docstatus=0) as status

# (select count(a.docstatus=0) from`tabASC` a where semis_code=s.name and a.level="Primary") as status	
	# sum(case when a.docstatus=0 then 1 else 0 end) as asc_total
							# from `tabSchool` s,
							# `tabASC` a
							# where s.name = a.semis_code and a.docstatus=1 
							# , as_dict=1
							# count(s.name) as level_total,
							# sum(case when s.level='Primary' then 1 else 0 end) as primary_total,
							# (select count(a.name) from`tabASC` a where a.level="Primary" and a.district=s.district) as primary_status,
def get_columns(filters):
	columns = [
		_("School level") + "::130",
		_("Urban Areas") + "::130",
		_("Rular Areas") + "::130",
		_("Total") + "::130",
		_("urban Areas Avg") + "::130",
		_("Rular Areas Avg") + "::130",
		_("Total Avg") + "::130",


	

	]
	return columns