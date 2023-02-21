# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _

def execute(filters=None):
	columns, data = [], []
	year = filters.get("year")
	columns = get_columns()	
	data = get_data(year)
	return columns, data

def get_data(year):
	data_ = frappe.db.sql(""" SELECT a.district, 
							SUM(enrol.boys) AS boys,
							d.boys,
							(case when d.parent = a.district then round(sum(enrol.boys)/ d.boys*100,2) else 0 end) as boys_per,
							SUM(enrol.girls) AS girls,
							d.girls,
							(case when d.parent = a.district then round(sum(enrol.girls)/ d.girls*100,2) else 0 end) as girls_per,
							SUM(enrol.boys)+SUM(enrol.girls) AS total_enroll,
							d.total_population,
							(case when d.parent = a.district then round((sum(enrol.boys) + SUM(enrol.girls)) / d.total_population*100,2) else 0 end) as per
							FROM `tabEnrolment Class and Gender wise` enrol 
							LEFT JOIN (select name, district, docstatus from `tabASC` where year=%s and docstatus!=2) a on enrol.parent = a.name
							CROSS JOIN `tabDistrict Population` d on d.parent = a.district
							group by a.district """,(year))
	return data_
def get_columns():
	columns = [
		_("District") + "::180",
		_("Boys Enrollment") + "::150",
		_("Boys Population") + "::150",
		_("Boys GER(%)") + "::150",
		_("Girls Enrollment") + "::150",
		_("Girls Population") + "::150",
		_("Girls GER(%)") + "::150",
		_("Total Enrollment") + "::150",
		_("Total Population") + "::150",
		_("Total GER(%)") + "::150"
		]
	return columns