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
	fac_ranking = frappe.db.sql("""Select Division,District,
	(SUM(CASE WHEN (`Classrooms` = 0) THEN 1 ELSE 0 END)), 
	(SUM(CASE WHEN (`Classrooms` = 1) THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 2) THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 3) THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 4)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 5)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 6)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 7)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 8)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` = 9)  THEN 1 ELSE 0 END)),
	(SUM(CASE WHEN (`Classrooms` >= 10) THEN 1 ELSE 0 END)),
	count(id)
	from `tabASC_KPI` 
    where 1 %s
    GROUP BY Division,District"""% conditions, filters)
	return fac_ranking

def get_conditions(filters):
	conditions=""
	if filters.get("year"):
		conditions += "  AND  Year = %(year)s"
	if filters.get("division"):
		conditions += "  AND  Division = %(division)s"
	if filters.get("district"):
			conditions += "  AND  District = %(district)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("level"):
		conditions = "  and Level = %(level)s"
	if filters.get("status"):
		conditions += "  and Status = %(status)s "
	if filters.get("gender"):
		conditions += "  and Gender = %(gender)s"
	return conditions, filters

def get_columns(filters):
	columns = [
		_("Division") + "::140",
		_("District") + "::140",
		_("Shelterless") + "::140",
		_("One") + "::140",
		_("Two") + "::140",
		_("Three") + "::140",
		_("Four") + "::140",
		_("Five") + "::140",
		_("Six") + "::140",
		_("Seven") + "::140",
		_("Eight") + "::140",
		_("Nine") + "::140",
		_("Ten and  More") + "::140",
		_("Total no. of Schools") + "::170",

		
		]
		
	return columns