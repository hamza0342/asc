# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		_("District") + "::140",
		_("Class I") + "::140",
		_("Class II") + "::140",
		_("Class III") + "::140",
		_("Class IV") + "::140",
		_("Class V") + "::140",
		_("Class VI") + "::140",
		_("Class VII") + "::140",
		_("Class VIII") + "::140",
		_("Class IX") + "::140",
		_("Class X") + "::140"
		# _("Class XI") + "::140",
		# _("Class XII") + "::140",


	]
	return columns

def get_data(filters):
	conditions, group_by = get_condition(filters)
	current_year = None
	last_year = None
	if filters.get("year") == "2021-22":
		current_year = '2021-22'
		last_year = '2020-21'
	elif filters.get("year") =="2020-21":
		current_year = '2020-21'
		last_year = '2018-19'
	elif filters.get("year") =="2018-19":
		current_year = '2018-19'
		last_year = '2016-17'
	elif filters.get("year") =="2016-17":
		current_year = '2016-17'
		last_year = '2015-16'

	temp_query = """Select District, 
	FORMAT( ( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-I Male`,0) + IFNULL(`Class-I Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Katchi Male`,0) + IFNULL(`Katchi Female`,0)) ELSE 0 END) ) *100 , 2) ,
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-II Male`,0) + IFNULL(`Class-II Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-I Male`,0) + IFNULL(`Class-I Female`,0)) ELSE 0 END) ) *100 , 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-III Male`,0) + IFNULL(`Class-III Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-II Male`,0) + IFNULL(`Class-II Female`,0)) ELSE 0 END) ) *100, 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-IV Male`,0) + IFNULL(`Class-IV Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-III Male`,0) + IFNULL(`Class-III Female`,0)) ELSE 0 END) ) *100, 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-V Male`,0) + IFNULL(`Class-V Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-IV Male`,0) + IFNULL(`Class-IV Female`,0)) ELSE 0 END) ) *100 , 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-VI Male`,0) + IFNULL(`Class-VI Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-V Male`,0) + IFNULL(`Class-V Female`,0)) ELSE 0 END) ) *100 , 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-VII Male`,0) + IFNULL(`Class-VII Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-VI Male`,0) + IFNULL(`Class-VI Female`,0)) ELSE 0 END) ) *100 , 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-VIII Male`,0) + IFNULL(`Class-VIII Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-VII Male`,0) + IFNULL(`Class-VII Female`,0)) ELSE 0 END) ) *100 , 2),
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-IX Male`,0) + IFNULL(`Class-IX Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-VIII Male`,0) + IFNULL(`Class-VIII Female`,0)) ELSE 0 END) ) *100, 2) ,
	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-X Male`,0) + IFNULL(`Class-X Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-IX Male`,0) + IFNULL(`Class-IX Female`,0)) ELSE 0 END) ) *100 , 2)
	

	from tabASC_KPI where Year is not NULL {condition}
	group by district
	""".format(current_year = current_year , last_year= last_year , condition= conditions)
	data_  = frappe.db.sql(temp_query,filters)
	
	return data_
# FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-XI Male`,0) + IFNULL(`Class-XI Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-X Male`,0) + IFNULL(`Class-X Female`,0)) ELSE 0 END) ) *100, 2) ,
# 	FORMAT(( SUM(CASE WHEN Year='{current_year}' THEN(IFNULL(`Class-XII Male`,0) + IFNULL(`Class-XII Female`,0)) ELSE 0 END) / SUM(CASE WHEN Year='{last_year}' THEN(IFNULL(`Class-XI Male`,0) + IFNULL(`Class-XI Female`,0)) ELSE 0 END) ) *100 , 2)
def get_condition(filters):
	conditions , group_by = "" , "GROUP BY region,district Order By region,district"
	# if filters.get("division"):
	# 	conditions += " AND region = %(division)s"
	# 	group_by = " GROUP BY region, district Order By region,district"

	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  Status = %(status)s"
	if filters.get("level"):
		conditions += " AND Level = %(level)s"
	if filters.get("enrollment")=='Male':
		conditions += " AND `Boys Enrollment` >0"
	elif filters.get("enrollment")=='Female':
		conditions += "AND `Girls Enrollment` >0"

	return conditions, group_by

