# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):

	columns = get_columns()
	conditions, filters = get_conditions(filters)
	data = get_data(filters.get("year"),filters.get("division"),filters.get("district"),filters.get("taluka"),filters.get("status"),conditions, filters)
	
	return columns, data

def get_data(year,division,district,taluka,status,conditions, filters):
	if year and not division and not district and not taluka and not status:
		fac_ranking = frappe.db.sql("""SELECT 
		CONCAT('<a Division=''',Division,''' Year=''','%s',''' type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"))''>',Division,'</a>') as ":Data:100",
		District,Tehsil,
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By District
	ORDER BY Division and District ASC"""% (year,conditions), filters)
		return fac_ranking
	if year and status and not division and not district and not taluka :
		fac_ranking = frappe.db.sql("""SELECT 
		CONCAT('<a Division=''',Division,''' Year=''','%s',''' Status=''','%s','''type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"),this.getAttribute("status") )''>',Division,'</a>') as ":Data:100",
		District,Tehsil,
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By District
	ORDER BY Division and District ASC"""% (year,status,conditions), filters)
		return fac_ranking
	if year and division and not district and not taluka and not status:
		fac_ranking = frappe.db.sql("""SELECT Division,
		CONCAT('<a District=''',District,''' Year=''','%s',''' Division=''','%s','''type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"),this.getAttribute("District"))''>',District,'</a>') as ":Data:100",
		Tehsil,
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By Tehsil
	ORDER BY Division and District ASC"""% (year,division,conditions), filters)
		return fac_ranking
	if year and division and status and not district and not taluka:
		fac_ranking = frappe.db.sql("""SELECT Division,
		CONCAT('<a District=''',District,''' Year=''','%s',''' Division=''','%s',''' Status=''','%s','''type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"),this.getAttribute("District"),this.getAttribute("status"))''>',District,'</a>') as ":Data:100",
		Tehsil,
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By Tehsil
	ORDER BY Division and District ASC"""% (year,division,status,conditions), filters)
		return fac_ranking
	if year and division and district and not taluka and not status:
		fac_ranking = frappe.db.sql("""SELECT Division,District,
		CONCAT('<a Tehsil=''',Tehsil,''' Year=''','%s',''' Division=''','%s',''' District=''','%s','''type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"),this.getAttribute("District"),this.getAttribute("Tehsil"))''>',Tehsil,'</a>') as ":Data:100",
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By Tehsil
	"""% (year,division,district,conditions), filters)
	# if year and division and district and taluka:
		return fac_ranking
	if year and division and district and status and not taluka :
		fac_ranking = frappe.db.sql("""SELECT Division,District,
		CONCAT('<a Tehsil=''',Tehsil,''' Year=''','%s',''' Division=''','%s',''' District=''','%s',''' Status=''','%s','''type=''button''  onClick=''open_report(this.getAttribute("Division"), this.getAttribute("Year"),this.getAttribute("District"),this.getAttribute("Tehsil"))''>',Tehsil,'</a>') as ":Data:100",
	SUM(
		CASE WHEN Level= "Primary" THEN 1 ELSE 0
		END
		) AS primary_school,
	SUM(
		CASE WHEN Level = "Middle" THEN 1 ELSE 0
		END
		) AS Middle,
	SUM(
		CASE WHEN Level = "Elementary" THEN 1 ELSE 0
		END
		) AS Elementary,
	SUM(
		CASE WHEN Level = "Secondary" THEN 1 ELSE 0
		END
		) AS Secondary,
	SUM(
		CASE WHEN Level = "Higher Secondary" THEN 1 ELSE 0
		END
		) AS higher_secondary

	from `tabASC_KPI`
	WHERE 1 %s
	Group By Tehsil
	"""% (year,division,district,status,conditions), filters)
	# if year and division and district and taluka:
		return fac_ranking

def get_conditions(filters):
	conditions=""
	if filters.get("year"):
		conditions += "  AND  Year = %(year)s"
	if filters.get("level1"):
		conditions = "  and Level = %(level1)s"
	if filters.get("status"):
		conditions += "  and Status = %(status)s "
	if filters.get("gender"):
		conditions += "  and Gender = %(gender)s"
	if filters.get("division"):
			conditions += "  AND  Division = %(division)s"
	if filters.get("district"):
			conditions += "  AND  District = %(district)s"
	if filters.get("taluka"):
			conditions += "  AND  Tehsil = %(taluka)s"
	return conditions, filters

def get_columns():
	columns = [
		_("Division") + "::150",
		_("District") + "::150",
		_("Taluka") + "::150",
		_("Primary School") + "::140",
		_("Middle School") + "::150",
		_("Elementary School") + "::150",
		_("Secondary School") + "::150",
		_("Higher Secondary School") + "::180"
		
		]
		
	return columns
