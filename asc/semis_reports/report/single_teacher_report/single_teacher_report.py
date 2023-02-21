# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
from pkgutil import get_data
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters)
	
	return columns, data
	
def get_columns():
	columns=[{
		"label":_("Division"),
		"fieldtype":"Data",
		"fieldname":"division",
		"options":"Division",
		"width": 150
	},{
		"label":_("District"),
		"fieldtype":"Data",
		"fieldname":"district",
		"options":"District",
		"width": 150
	},{
		"label":_("Total Schools"),
		"fieldtype":"Int",
		"fieldname":"total_School",
		"width": 150
	},{
		"label":_("Single Teacher Schools "),
		"fieldtype":"Int",
		"fieldname":"Teacher(Number)", 
		"width": 150
	},{
		"label":_("Single Teacher School(%) "),
		"fieldtype":"Percent ",
		"fieldname":"Teacher(%)", 
		"width": 150
	}
	,{
		"label":_(" Male Single Teacher Schools "),
		"fieldtype":"Int",
		"fieldname":"teacher_Male(Number)", 
		"width": 150
	},{
		"label":_("Male Single Teacher School(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_Male(%) ", 
		"width": 150
	},{
		"label":_("Female Single Teacher  Schools "),
		"fieldtype":"Int",
		"fieldname":"teacher_female(Number)", 
		"width": 150
	},{
		"label":_("Female Single Teacher School(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_female(%)", 
		"width": 150
	},{
		"label":_("Mixed Single Teacher Schools"),
		"fieldtype":"Int",
		"fieldname":"teacher_mixed(Number)", 
		"width": 150
	},{
		"label":_("Mixed Single Teacher School(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_mixed(%)", 
		"width": 150
	}
	]
	return columns
	
def get_data(filters):
	conditions= get_condition(filters)
	query=""" (Select region, district,count(name) ,
	SUM(CASE WHEN total_teacher=1 then 1 else 0 end),
 	round(( SUM(CASE WHEN total_teacher=1 then 1 else 0 end)/count(name) * 100 ),2) ,
    SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end ),
    round(( SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end )/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2)
	FROM tabASC 
	WHERE docstatus != 2  %s
	GROUP BY  district)
	Union All(
	Select "Total", "",count(name) ,
	SUM(CASE WHEN total_teacher=1 then 1 else 0 end),
 	round(( SUM(CASE WHEN total_teacher=1 then 1 else 0 end)/count(name) * 100 ),2) ,
    SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end ),
    round(( SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end )/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2)
	FROM tabASC 
	WHERE docstatus != 2  %s
	) """ % (conditions,conditions)
	#frappe.msgprint(query)
	info = frappe.db.sql(query, filters)
	return info



def get_condition(filters):
	conditions = ""
	if filters.get("division"):
		conditions += " AND  region = %(division)s"
		group_by = "GROUP BY  t.region,  district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("level"):
		conditions += " AND level = %(level)s"
	return conditions
