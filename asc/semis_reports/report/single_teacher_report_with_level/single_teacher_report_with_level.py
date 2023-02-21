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
		"label":_("Level"),
		"fieldtype":"link",
		"fieldname":"level",
		"options":"Level",
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
		"width": 180
	},{
		"label":_("Single Teacher Schools(%) "),
		"fieldtype":"Percent ",
		"fieldname":"Teacher(%)", 
		"width": 230
	}
	,{
		"label":_("Boys Single Teacher Schools "),
		"fieldtype":"Int",
		"fieldname":"teacher_Male(Number)", 
		"width": 220
	},{
		"label":_("Boys Single Teacher Schools(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_Male(%) ", 
		"width": 230
	},{
		"label":_("Girls Single Teacher Schools "),
		"fieldtype":"Int",
		"fieldname":"teacher_female(Number)", 
		"width": 220
	},{
		"label":_("Girls Single Teacher Schools(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_female(%)", 
		"width": 230
	},{
		"label":_("Mixed Single Teacher Schools"),
		"fieldtype":"Int",
		"fieldname":"teacher_mixed(Number)", 
		"width": 220
	},{
		"label":_("Mixed Single Teacher Schools(%) "),
		"fieldtype":"Percent",
		"fieldname":"teacher_mixed(%)", 
		"width": 250
	}
	]
	return columns
	
def get_data(filters):
	conditions= get_condition(filters)
	query=""" (Select level,count(tabASC.name) ,
	SUM(CASE WHEN total_teacher=1 then 1 else 0 end),
 	round((  SUM(CASE WHEN total_teacher=1 then 1 else 0 end)/count(tabASC.name) * 100 ) ,1) ,
    SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end ),
    round(( SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end )/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2)
	FROM tabASC Left JOIN tabLevel ON tabASC.level=tabLevel.name
	WHERE tabASC.docstatus != 2  %s
	GROUP BY  tabASC.level ORDER BY tabLevel.list_order)
	UNION ALL
	(Select "Total",count(tabASC.name) ,
	SUM(CASE WHEN total_teacher=1 then 1 else 0 end),
 	round((  SUM(CASE WHEN total_teacher=1 then 1 else 0 end)/count(tabASC.name) * 100 ) ,1) ,
    SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end ),
    round(( SUM( case when total_teacher=1 and school_gender='Boys' then 1 else 0 end )/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Girls' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2),
    SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end),
    round(( SUM(case when total_teacher=1  and school_gender='Mixed' then 1 else 0 end)/SUM(CASE WHEN total_teacher=1 then 1 else 0 end) * 100 ),2)
	FROM tabASC Left JOIN tabLevel ON tabASC.level=tabLevel.name
	WHERE tabASC.docstatus != 2  %s ORDER BY tabLevel.list_order) """ % (conditions,conditions)
	#frappe.msgprint(query)
	info = frappe.db.sql(query, filters)
	return info



def get_condition(filters):
	conditions = ""
	if filters.get("division"):
		conditions += " AND  region = %(division)s"
		# group_by = "GROUP BY  t.region,  district"
	if filters.get("year"):
		conditions += "  AND  year = %(year)s"
	if filters.get("location"):
		conditions += "  AND  location = %(location)s"
	if filters.get("status"):
		conditions += "  AND  status_detail = %(status)s"
	if filters.get("district"):
		conditions += " AND district = %(district)s"
	return conditions
