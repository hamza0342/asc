 # Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	if not filters: filters = {}
	
	columns = get_columns(filters)
	districtdata_data = get_level_wise(filters)
	# print(filters.get("level"))
	# filters.get("level")
	
	
	return columns, districtdata_data

def get_level_wise(filters):
	# frappe.msgprint(frappe.as_json(filters.year))
	schools = frappe.db.sql("""select sch.district,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 1 and district=sch.district) as oneroom,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 2 and district=sch.district) as tworooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 3 and district=sch.district) as threerooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 4 and district=sch.district) as fourrooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 5 and district=sch.district) as fiverooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 6 and district=sch.district) as sixrooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 7 and district=sch.district) as sevenrooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 8 and district=sch.district) as eightrooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school= 9 and district=sch.district) as ninerooms,
							(select count(name) from `tabASC` where availability_of_building='Yes' and total_rooms_school>= 9 and district=sch.district) as tenandmore,
							(select count(name) from `tabASC` where availability_of_building='Yes' and district=sch.district) as Totalschool
							
							from `tabASC` as sch 
							group by sch.district""")

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
							# count(sch.level) as total,
							# round(((select count(level) from `tabSchool` where location='Urban' and level=sch.level)/(select count(level) from `tabSchool`)*100),2) as UrbanAvg,
							# round(((select count(level) from `tabSchool` where location='Rural' and level=sch.level)/(select count(level) from `tabSchool`)*100),2) as RuralAvg,
							# round((count(sch.level)/(select count(level) from `tabSchool`)*100),2) as TotalAvg
							# 
							# ,
							# count(sch.level) as total,
							#
							#
							# round(((select count(sch.level) from `tabASC` where sch.availability_of_building='No' and sch.no_relevant_code='Hut' and level=sch.level)/(select count(level) from `tabASC`)*100),2) as hutpersentage,
							# round(((select count(sch.level) from `tabASC` where sch.availability_of_building='No' and sch.no_relevant_code='No Info' and level=sch.level)/(select count(level) from `tabASC`)*100),2) as noinfopersentage,
							# round(((select count(sch.level) from `tabASC` where sch.availability_of_building='No' and sch.no_relevant_code='Other and level=sch.level)/(select count(level) from `tabASC`)*100),2) as otherpersentage,
							# round((select count(name) from`tabASC` where availability_of_building='No' and level=sch.level)/(select count(name) from `tabASC`  where availability_of_building='No' and level=sch.level)*100),2) as TotalAvg
					
		# 
		# 
		# 
		# 
		#
		#
		#
		
		# _("Persentage (Total)") + "::130",
def get_columns(filters):
	columns = [
		_("District") + "::100",
		_("One Room") + "::80",
		_("Two Room") + "::80",
		_("Three Room") + "::80",
		_("Four Room") + "::80",
		_("Five Room") + "::80",
		_("Six Room") + "::80",
		_("Seven Room") + "::80",
		_("Eight Room") + "::80",
		_("Nine Room") + "::80",
		_("Ten and More") + "::80",
		_("Total School in district") + "::130",
	
		
	]
	return columns