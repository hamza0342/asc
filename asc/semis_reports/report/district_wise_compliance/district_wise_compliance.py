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
	schools = frappe.db.sql("""select 
							s.district,
							count(s.name) as level_total,
							sum(case when s.level='Primary' then 1 else 0 end) as primary_total,
							(select count(a.name) from`tabASC` a where a.level="Primary" and a.district=s.district) as primary_status,
							sum(case when s.level='Middle' then 1 else 0 end) as Middle_total,
							(select count(a.name) from`tabASC` a where a.level="Middle" and a.district=s.district) as middle_status,
							sum(case when s.level='Elementary' then 1 else 0 end) as Elementary_total,
							(select count(a.name) from`tabASC` a where a.level="Elementary" and a.district=s.district) as elementry_status,
							sum(case when s.level='Secondary' then 1 else 0 end) as Secondary_total,
							(select count(a.name) from`tabASC` a where a.level="Secondary" and a.district=s.district) as secondary_status,
							sum(case when s.level='Higher Secondary' then 1 else 0 end) as highersecondary_total,
							(select count(a.name) from`tabASC` a where a.level="Higher Secondary" and a.district=s.district) as status		
							from `tabSchool` s
							where s.docstatus = 0
							group by s.district """ )

	return schools
# WHERE docstatus=1 and docstatus=2 as_dict=1
#  count(a.docstatus=0) as status

# (select count(a.docstatus=0) from`tabASC` a where semis_code=s.name and a.level="Primary") as status	
	# sum(case when a.docstatus=0 then 1 else 0 end) as asc_total
							# from `tabSchool` s,
							# `tabASC` a
							# where s.name = a.semis_code and a.docstatus=1 
							# , as_dict=1
def get_columns(filters):
	columns = [
		_("District Name") + "::130",		
		_("Total Primary") + "::180",
		_("census completed Primary") + "::180",
		_("Total Middle") + "::180",
		_("census completed Middle") + "::180",
		_("Total Elementary") + "::180",
		_("census completed Elementary") + "::180",
		_("Total Secondary") + "::180",
		_("census completed Secondary") + "::180",
		_("Total Higher Secondary") + "::180",
		_("census completed Higher Secondary") + "::180",
	

	]
	return columns
	# select 
	# 						s.district,
	# 						count(s.name),(select count(name) from `tabASC` where docstatus=1 and s.level="Primary"),
	# 						count(s.name),(select count(name) from `tabASC` where docstatus=1 and s.level="Middle"),
	# 						count(s.name),(select count(name) from `tabASC` where docstatus=1 and s.level="Elementary"),
	# 						count(s.name),(select count(name) from `tabASC` where docstatus=1 and s.level="Secondary"),
	# 						count(s.name),(select count(name) from `tabASC` where docstatus=1 and s.level="Higher Secondary")
	# 						from `tabSchool` s
	# 						group by s.district