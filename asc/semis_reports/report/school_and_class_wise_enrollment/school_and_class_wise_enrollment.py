# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns,col_string= get_columns(filters)
	data = get_data(filters,col_string)
	return columns, data 

def get_columns(filters):
	col_string=""
	columns=[]
	# if filters.get("division") and not filters.get("district"):
	# 	col_string=" district , tehsil ,"
	# 	columns.extend((_("Disrict") + "::130" ,
	# 					_("Taluka") + "::130"))
	# if filters.get("district"):
	# 	col_string=" tehsil ,"
	# 	columns.append(_("Taluka") + "::130")
	columns.extend( (
		_("Semis Code") + "::100",
		_("School Name") + "::200",
		_("Division") + "::130" ,
		_("Disrict") + "::130" ,
		_("Taluka") + "::130",
		_("School Gender") + "::130",
		_("School Level") + "::130",
		_("ECCE Male") + "::130",
		_("ECCE Female") + "::130",
		_("Katchi Male") + "::130",
		_("Katchi Female") + "::130",
		_("Class-I Male") + "::130",
		_("Class-I Female") + "::130",	
		_("Class-II Male") + "::130",
		_("Class-II Female") + "::130",
		_("Class-III Male") + "::130",
		_("Class-III Female") + "::130",		
		_("Class-IV Male") + "::130",
		_("Class-IV Female") + "::130",		
		_("Class-V Male") + "::130",
		_("Class-V Female") + "::130",	
		_("Class-VI Male") + "::130",
		_("Class-VI Female") + "::130",
		_("Class-VII Male") + "::130",
		_("Class-VII Female") + "::130",
		_("Class-VIII Male") + "::130",
		_("Class-VIII Female") + "::130",
		_("Class-IX Male") + "::130",
		_("Class-IX Female") + "::130",
		_("Class-X Male") + "::130",
		_("Class-X Female") + "::130",	
		_("Class-XI Male") + "::130",
		_("Class-XI Female") + "::130",
		_("Class-XII Male") + "::130",
		_("Class-XII Female") + "::130",				
	))
	return columns , col_string

def get_data(filters,col_string):
	cond= get_condition(filters)
	temp_query = """ Select
        `semis_code`,
        `school_name`,
		`division`,
		`district`,
		`tehsil`,
        `gender`,
		`level`,
        `ecce_male`,
        `ecce_female`,
        `katchi_male`,
        `katchi_female`,
        `class_1_male`,
        `class_1_female`,
        `class_2_male`,
        `class_2_female`,
        `class_3_male`,
        `class_3_female`,
        `class_4_male`,
        `class_4_female`,
        `class_5_male`,
        `class_5_female`,
        `class_6_male`,
        `class_6_female`,
        `class_7_male`,
        `class_7_female`,
        `class_8_male`,
        `class_8_female`,
        `class_9_male`,
        `class_9_female`,
        `class_10_male`,
        `class_10_female`,
        `class_11_male`,
        `class_11_female`,
        `class_12_male`,
        `class_12_female` from tabASC_KPI where name IS NOT NULL %s
		order by division, district, tehsil
	"""%(cond)
	data = frappe.db.sql(temp_query,filters)
	return data

def get_condition(filters):
	conditions = ""
	if filters.get("division"):
		conditions += " AND division = %(division)s"
		# group_by = "GROUP BY  t.region,  district"
	if filters.get("year"):
		conditions += "  AND year = %(year)s"
	# if filters.get("location"):
	# 	conditions += "  AND location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status = %(status)s"
	if filters.get("district"):
		conditions += " AND district = %(district)s"
	if filters.get("taluka"):
		conditions += " AND tehsil = %(taluka)s"
	if filters.get("level"):
		conditions += " AND level = %(level)s"
	return conditions