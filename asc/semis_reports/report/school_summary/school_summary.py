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
	fac_ranking = frappe.db.sql("""SELECT Division,District,
SUM(CASE WHEN Gender = "Boys" THEN 1 ELSE 0 END) AS Boys,
SUM(CASE WHEN Gender = "Girls" THEN 1 ELSE 0 END) AS Girls,
SUM(CASE WHEN Gender = "Mixed" THEN 1 ELSE 0 END) AS Mixed,
Count(id),
SUM( `Boys Enrollment` ) AS Boys_enrollment,
SUM( `Girls Enrollment` ) AS Girls_enrollment,
SUM( `Total Enrollment` ) AS Total_enrollment,
SUM( `Male Teachers` ) AS male_teacher,
SUM( `Female Teachers` ) AS female_teacher,
SUM( `Total Teachers` ) AS total_teacher,
SUM(`Classrooms` ) as Classrooms_school

from `tabASC_KPI`
WHERE 1 %s
Group By Division , District
ORDER BY Division , District ASC"""% conditions, filters)

	return fac_ranking
frappe.throw(frappe.as_json(fac_ranking))
def get_conditions(filters):
	conditions=""
	if filters.get("year"):
		conditions += "  AND  Year = %(year)s"
	if filters.get("level1"):
		conditions = "  and Level = %(level1)s"
	if filters.get("status"):
		conditions += "  and Status = %(status)s "
	if filters.get("gender"):
		conditions += "  and Gender = %(gender)s"
	if filters.get("location"):
		conditions += "  and Location = %(location)s"
	return conditions, filters

def get_columns(filters):
	columns = [
		_("Division") + "::150",
		_("District") + "::150",
		_("Boys") + "::140",
		_("Girls") + "::150",
		_("Mixed") + "::150",
		_("Total") + "::150",
		_("Boys Enrollment") + "::150",
		_("Girls Enrollment") + "::150",
		_("Total Enrollment") + "::150",
		_("Male Teacher") + "::150",
		_("Female Teacher") + "::150",
		_("Total Teacher") + "::150",
		_("Total Rooms") + "::150",
		
		]
		
	return columns
