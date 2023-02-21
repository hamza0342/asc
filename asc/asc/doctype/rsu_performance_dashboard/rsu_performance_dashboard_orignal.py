# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RSUPerformanceDashboard(Document):
	pass


@frappe.whitelist()
def get_data():
	default_year=frappe.db.get_single_value("ASC Panel", "default_year")
	district_string = get_district()
	final_data=[]
	total_schools= get_total_schools()

	assigned_total_schools = get_total_assigned_schools(default_year)
	assigned_district=get_assigned_district(default_year)
	assigned_district_list=get_total_assigned_schools_list(default_year)
	schools_string=""
	count = 1
	flag=0
	length=len(assigned_district_list)
	for scl in assigned_district_list:
		if count == 1:
			schools_string += "and ( semis_code = %s "%(scl)
			count+=1
		else:
			schools_string += " OR semis_code = %s "%(scl)
		flag=flag+1
		if(flag==length):
			schools_string+=" )"


			
	completed_district=get_completed_district(default_year,schools_string)
	asc_query= """SELECT IFNULL(SUM(CASE WHEN docstatus=0 AND completion_check=1 THEN 1 ELSE 0 END),0) AS completed,IFNULL(SUM(CASE WHEN docstatus=0 AND completion_check=0 THEN 1 ELSE 0 END),0) AS not_completed,IFNULL(SUM(CASE WHEN docstatus=1 THEN 1 ELSE 0 END),0) AS verified FROM tabASC where  year='%s'  """%(default_year)
	asc_query = frappe.db.sql(asc_query, as_dict=1) 
	
	final_data.append(total_schools)
	final_data.append(assigned_total_schools)
	final_data.append(asc_query)
	final_data.append(district_string)
	final_data.append(assigned_district)
	final_data.append(completed_district)

	return final_data





def get_district():
	temp_query = """Select name as district FROM `tabDistrict` order by name"""
	district = frappe.db.sql(temp_query)
	return district

def get_assigned_district(default_year):
	temp_query="SELECT district, count(name) as assigned_district  FROM `tabSchool` where enabled=1 group by district"""
	district = frappe.db.sql(temp_query,as_dict=1)
	return district

def get_completed_district(default_year,school_string):
	temp_query= """SELECT district, SUM(CASE WHEN docstatus=0 AND completion_check=1 THEN 1 ELSE 0 END) AS completed,SUM(CASE WHEN docstatus=0 AND completion_check=0 THEN 1 ELSE 0 END) AS not_completed,SUM(CASE WHEN docstatus=1 THEN 1 ELSE 0 END) AS verified FROM tabASC where  year='%s'  group by district """%(default_year)
	district = frappe.db.sql(temp_query,as_dict=1)
	return district

def get_total_assigned_schools(default_year):
	temp_query = """SELECT count(name) as assigned_schools FROM `tabASC` where year='2021-22' """
	assigned_total_schools = frappe.db.sql(temp_query, as_dict=1)[0]
	return assigned_total_schools
def get_total_assigned_schools_list(default_year):
	temp_query = """SELECT distinct(per.school) FROM `tabASC Roster` ros inner join `tabSchool Permission` per on ros.name = per.parent where ros.year='%s'"""%(default_year)
	assigned_total_schools = frappe.db.sql(temp_query)
	return assigned_total_schools



def get_total_schools():
    temp_query= """SELECT count(name) AS total_schools, SUM(CASE WHEN name = tid THEN 1 ELSE 0 END) AS tid_school FROM tabSchool where enabled = 1"""
    total_schools = frappe.db.sql(temp_query,as_dict=1)
    return total_schools

def get_user_count(default_year, data):
	users = []
	for d in data:
		users = d['user']
	for user_ in users:
		temp_query = """SELECT distinct(per.school) FROM `tabASC Roster` ros inner join `tabSchool Permission` per on ros.name = per.parent where ros.year='%s' AND ros.user = '%s' """%(default_year,str(user_))
		result = frappe.db.sql(temp_query, as_dist=1)
		return result
