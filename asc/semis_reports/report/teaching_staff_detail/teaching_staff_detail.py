# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	columns=[
		_("Personal ID") + "::140",
		_("Name") + "::170",
		_("Gender") + "::170",
		_("Qualification") + "::170",
		_("Designation") + "::140",
		_("Grade") + "::120",
		_("CNIC") + "::150",
		_("Biometric Registered") + "::170",
	]
	return columns


def get_data(filters):
	year = filters.get("year")
	school = filters.get("school")
	asc_name = frappe.db.sql("Select name from tabASC where year = '%s' and semis_code = '%s' "%(year,school))
	if asc_name:
		temp_query = "SELECT  p_num_ag_office,full_n,gender,h_academic_qualification, designation_code, bps_current, cnic,b_registered  FROM `tabWorking Teaching Staff Detail` WHERE docstatus != 2 and `asc` = '%s' " % (asc_name[0][0])
		info = frappe.db.sql(temp_query, filters)
		return info

