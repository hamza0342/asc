import frappe
@frappe.whitelist()
def get_data(division = None, year = None, level=None, school_gender=None, location=None):
	condition = " and census.year= '%s' " % str(year)
	if division:
		condition += " and census.region= '%s' " % str(division)
	if level:
		condition += " and census.level= '%s' " % str(level)
	if school_gender:
		condition += " and census.school_gender= '%s' " % str(school_gender)
	if location:
		condition += " and census.location= '%s' " % str(location)
	data_ = frappe.db.sql("""select census.district as name, count(census.name) as Total_Schools, sum(case when e.class is NOT null and e.total_class then 1 else 0 END) as ECE_Schools,  sum(case when e.class is NOT null and e.total_class then 0 else 1 END) as No_ECE_Schools,(sum(case when e.class is NOT null and e.total_class then 1 else 0 END)/count(census.name))*100 as value, d.path_features as path FROM `tabASC` census left JOIN `tabEnrolment Class and Gender wise` e ON census.name = e.parent JOIN tabDistrict d on census.district=d.name WHERE census.docstatus!=2 %s AND e.class='ECE' GROUP BY census.district """% (condition), as_dict=1)
	return data_