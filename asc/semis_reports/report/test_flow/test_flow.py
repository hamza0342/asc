# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	frappe.msgprint(frappe.as_json(filters))
	columns = get_columns()
	conditions, filters = get_conditions(filters)
	data = get_data(filters.get("year"),conditions, filters)
	
	return columns, data

def get_data(year,conditions, filters):
	fac_ranking = frappe.db.sql("""SELECT 
	 CONCAT('<a District=''',District,''' Year=''','%s',''' type=''button''  onClick=''open_report(this.getAttribute("District"), this.getAttribute("Year"))''>',District,'</a>') as ":Data:100",
ROUND(SUM(CASE WHEN Rooms=0 THEN 0 ELSe 1 end)/COUNT(DISTINCT id) *100,2) as having_building,
ROUND(SUM(IF(`Condition of Boundary Wall` = 'No Boundary Wall' OR `Condition of Boundary Wall` = '' OR `Condition of Boundary Wall` IS NULL,0,1))/COUNT(DISTINCT id) *100 ,2)AS boundary_wall,
ROUND(SUM(IF(`Electricity` = 'No Electricity Connection' OR `Electricity` = '' OR `Electricity` IS NULL,0,1))/COUNT(DISTINCT id) *100,2) AS Electricity,
ROUND(SUM(IF(`Water` = 'Yes' ,1,0))/COUNT(DISTINCT id) *100,2)  AS drinking_water,
ROUND(SUM(IF(`Toilet` = 'No' OR `Toilet` = '' OR `Toilet` IS NULL,0,1))/COUNT(DISTINCT id) *100,2) AS Toilet,
ROUND(SUM(IF(`Hand Wash` = 'No' OR `Hand Wash` = '' OR `Hand Wash` IS NULL,0,1))/COUNT(DISTINCT id) *100,2) AS hand_wash_facility

from `tabASC_KPI`
WHERE 1 %s
Group By District
ORDER BY Division and District ASC"""% (year,conditions), filters)
	return fac_ranking
def get_conditions(filters):
		conditions=""
		if filters.get("year"):
			conditions+="And Year=%(year)s"
		if filters.get("district"):
			conditions += "  AND  District = %(district)s"
		return conditions, filters

def get_columns():
	columns = [
		_("District") + "::150",
		_("Building") + "::140",
		_("Boundary Wall") + "::150",
		_("Electricity") + "::150",
		_("Drinking Water") + "::150",
		_("Toilets") + "::150",
		_("Hand Wash") + "::150"
		
		]
		
	return columns
