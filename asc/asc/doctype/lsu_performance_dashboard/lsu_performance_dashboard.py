# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LSUPerformanceDashboard(Document):
	pass


@frappe.whitelist()
def get_data():
	default_year=frappe.db.get_single_value("ASC Panel", "default_year")
	current_user = frappe.session.user
	district_string = get_district(current_user)

	total_schools= get_total_schools(district_string)
	
	asigned_schools = """SELECT Count(distinct(per.school)) as assigned_schools FROM `tabASC Roster` ros 
	inner join `tabSchool Permission` per on ros.name = per.parent 
	where ros.year='%s' AND (%s) order by per.planned_date"""%(default_year,district_string)
	asigned_schools = frappe.db.sql(asigned_schools, as_dict=1)

	asc_data=[]
	user_table_data =[]
	if asigned_schools[0]['assigned_schools']>0:
		assigned_total_schools = get_total_assigned_schools(default_year,district_string)
		user_table_data,asc_data = get_user_count(default_year,assigned_total_schools)
	else:
		asc_data.append({'completed':0 , 'not_completed':0 ,'verified':0})


	data=[]
	data.append(asigned_schools)
	data.append(user_table_data)
	data.append(total_schools[0])
	data.append(asc_data[0])

	return data





def get_district(current_user):
	temp_query = """Select for_value FROM `tabUser Permission` where user = '%s' AND allow = "District" """%(current_user)
	district = frappe.db.sql(temp_query)
	district_string=''
	if district:
		count = 1
		for dis in district:
			for d in dis:
				if count == 1:
					district_string += " district = '%s'"%(str(d))
					count+=1
				else:
					district_string += " OR district = '%s'"%(str(d))
	else:
		district_string +=" district = 'Badin' "
		
	return district_string

def get_total_assigned_schools(default_year,district_string):
	temp_query = """SELECT user,user_name,Count(distinct(per.school)) as assigned FROM `tabASC Roster` ros 
	inner join `tabSchool Permission` per on ros.name = per.parent 
	where ros.year='%s' AND (%s) GROUP BY user order by per.planned_date """%(default_year,district_string)
	assigned_total_schools = frappe.db.sql(temp_query, as_dict=1)
	return assigned_total_schools




def get_total_schools(district_string):
    temp_query= """SELECT count(name) AS total_schools, SUM(CASE WHEN name = tid THEN 1 ELSE 0 END) AS tid_schools FROM tabSchool where %s And enabled = 1"""%(district_string)
    total_schools = frappe.db.sql(temp_query,as_dict=1)
    return total_schools

def get_user_count(default_year, data):
	users = []
	asc_schools_string=""
	asc_count=1
	for d in data:
		users.append(d['user'])
	schools = []
	for user_ in users:
		temp_query = """SELECT distinct(per.school) FROM `tabASC Roster` ros inner join `tabSchool Permission` per on ros.name = per.parent where ros.year='%s' AND ros.user = '%s' """%(default_year,str(user_))
		schools = frappe.db.sql(temp_query)
		
		count = 1
		schools_string=""
		for scl in schools:
			if count == 1:
				schools_string += " semis_code = %s "%(scl)
				count+=1
			else:
				schools_string += " OR semis_code = %s "%(scl)

		for scl in schools:
			if asc_count == 1:
				asc_schools_string += " semis_code = %s "%(scl)
				asc_count+=1
			else:
				asc_schools_string += " OR semis_code = %s "%(scl)

		temp_query= """SELECT SUM(CASE WHEN completion_check = 1 AND docstatus=0 AND (%s) Then 1 Else 0 End ) AS user_completed_schools,SUM(CASE WHEN docstatus = 0 AND completion_check = 0 AND (%s)  THEN 1 ELSE 0 END) AS user_not_completed,SUM(CASE WHEN  docstatus=1 AND (%s) Then 1 Else 0 End ) AS user_verified_schools FROM tabASC where year = '%s' """%(schools_string,schools_string,schools_string,default_year)
	
		schools_count = frappe.db.sql(temp_query, as_dict=1)
		for d in data:
			for row in schools_count:
				if d['user'] == user_:
					d.update(row)			
	asc_query= """SELECT SUM(CASE WHEN docstatus=0 AND completion_check = 1 AND (%s) THEN 1 ELSE 0 END) AS completed,SUM(CASE WHEN docstatus = 0 AND completion_check = 0 AND (%s) THEN 1 ELSE 0 END) AS not_completed,SUM(CASE WHEN docstatus=1 AND (%s) THEN 1 ELSE 0 END) AS verified FROM tabASC where  year='%s' """%(asc_schools_string,asc_schools_string,asc_schools_string,default_year)
	asc_data = frappe.db.sql(asc_query, as_dict=1)

	return data,asc_data