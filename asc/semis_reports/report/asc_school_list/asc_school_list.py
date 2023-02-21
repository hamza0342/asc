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
	smc_fund = frappe.db.sql("""SELECT `SEMIS Code`,Division,
							District, Tehsil, `School Name`, Location, Gender, Level, Status,
							`Building Availability`, `Building Ownership`,`Building Condition`,
							Rooms, `Post Primary`, `Primary`, ECCE, Classrooms, Water, Electricity,
							`Condition of Boundary Wall`, Toilet, `Hand Wash`, `MHM Facility`, isCampus, 
							`No. of Merged Schools`, `Boys Enrollment`, `Girls Enrollment`, `Total Enrollment`,
							`Sindhi Enrollment`, `Urdu Enrollment`, `English Enrollment`, `Male Teachers`, 
							`Female Teachers`,`Total Teachers`
							from tabASC_KPI 
							WHERE  1 %s """% conditions, filters)
	return smc_fund

def get_conditions(filters):
	conditions=""
	if filters.get("year"):
		conditions = "  and Year = %(year)s"
	if filters.get("division"):
		conditions += "  and Division = %(division)s"
	if filters.get("district"):
		conditions += "  and District = %(district)s "
	if filters.get("level"):
		conditions += "  AND  Level = %(level)s "
	if filters.get("school_gender"):
		conditions += "  and Gender = %(school_gender)s"
	if filters.get("water_available"):
		conditions += "  and Water = %(water_available)s"
	if filters.get("electricity_connection"):
		conditions += "  and Electricity = %(electricity_connection)s"
	if filters.get("condition_of_building"):
		conditions += "  and `Building Condition` = %(condition_of_building)s"
	if filters.get("building_availability"):
		conditions += "  and `Building Availability` = %(building_availability)s"
	if filters.get("status"):
		conditions += "  and `Status` = %(status)s"
	if filters.get("location"):
		conditions += "  and Location = %(location)s"
	return conditions, filters

def get_columns(filters):
	columns = [
		_("SEMIS Code") + "::120",
		_("Division") + ":Link/Division:120",
		_("District") + ":Link/District:120",
		_("Taluka") + "::120",
		_("School Name") + "::120",
		_("Location") + "::120",
		_("Gender") + "::120",
		_("Level") + "::130",
		_("Status") + "::130",
		_("Building Availability") + "::120",
		_("Building Ownership") + "::160",
		_("Building Condition") + "::220",
		_("Rooms") + "::120",
		_("Post Primary") + "::120",
		_("Primary") + "::120",
		_("ECCE") + "::130",
		_("Classrooms") + "::120",
		_("Water") + "::160",
		_("Electricity") + "::220",
		_("Condition of Boundary Wall") + "::120",
		_("Toilet") + "::120",
		_("Hand Wash") + "::120",
		_("MHM Facility") + "::120",
		_("isCampus") + "::130",
		_("No. of Merged Schools") + "::130",
		_("Boys Enrollment") + "::120",
		_("Girls Enrollment") + "::160",
		_("Total Enrollment") + "::220",
		_("Sindhi Enrollment") + "::120",
		_("Urdu Enrollment") + "::130",
		_("English Enrollment") + "::130",
		_("Male Teachers") + "::120",
		_("Female Teachers") + "::160",
		_("Total Teachers") + "::220"
		]
		
	return columns

# @frappe.whitelist()
# def districts_user(user):
# 	district = frappe.db.sql("select for_value from `tabUser Permission` where user=%s", (user), as_dict=True)[0]
# 	return district