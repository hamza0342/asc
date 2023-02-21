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
		_("District") + "::100",

		_("Functional") + "::100",
		_("Non-Functional") + "::140",
		_("Total Schools") + "::140",


		_("Boys (Functional)") + "::140",
		_("Girls (Functional)") + "::140",
		_("Mixed (Functional)") + "::160",
		_("Total (Functional)") + "::140",
		_("Shelterless (Functional)") + "::200",
		_("Single room (Functional)") + "::200",

		_("Boys Enrollment") + "::130",
		_("Girls Enrollment") + "::130",
		_("Total Enrollment") + "::130",

		_("Male Teachers") + "::130",
		_("Female Teachers") + "::150",
		_("Total Teachers") + "::130",

		_("STR") + "::80",

		_("Water") + "::100",
		_("Electricity") + "::100",
		_("Boundary Wall") + "::130",
		_("Toilet") + "::100",
	]
	return columns


def get_data(filters):

	conditions , group_by = "", "GROUP BY district Order By district"
	if filters.get("division"):
		conditions += "  and region = %(division)s"
		group_by = "GROUP BY region, district Order By region,district "
	if filters.get("year"):
		conditions += "  and year = %(year)s"


	temp_query= """(Select district,
	SUM(
		CASE WHEN status_detail = "Functional" THEN 1 ELSE 0
	END
	),
	SUM(
		CASE WHEN status_detail = "Closed" THEN 1 ELSE 0
	END
	),
	Count(*),
	
	SUM(
	CASE WHEN tac.school_gender = "Boys" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Boys,
	SUM(
	CASE WHEN tac.school_gender = "Girls" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Girls,
	SUM(
	CASE WHEN tac.school_gender = "Mixed" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Mixed,
	SUM(
		CASE WHEN status_detail = "Functional" THEN 1 ELSE 0
	END
	),
	SUM(CASE WHEN total_rooms_school=0  and status_detail= 'Functional' THEN 1 ELSe 0 end) as Shelterless,
	SUM(CASE WHEN status_detail= 'Functional' and total_rooms_school = 1 then 1 else 0 end) as Rooms,



	SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(male_enrollment,0) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(female_enrollment,0) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_enrollment,0) ELSE 0
	END
	),


	SUM(
		CASE WHEN status_detail = "Functional" THEN (coalesce(govt_male_teachers,0) + coalesce(non_govt_male_teachers,0) )  ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN (coalesce(govt_male_teachers,0) + coalesce(non_govt_male_teachers,0)) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_teacher,0) ELSE 0
	END
	),



	Round( coalesce( (SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_enrollment,0) ELSE 0
	END
	)/SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_teacher,0) ELSE 0
	END
	)
                     ) ,0),0),


	SUM(
	IF(
		water_available = 'Yes' and status_detail= 'Functional' ,
		1,
		0
	)
	)  AS drinking_water,
	SUM(
	IF(
		(electricity_connection = 'WAPDA/KE' OR electricity_connection = 'Solar System') and status_detail = 'Functional',
		1,
		0
	)
	) AS Electricity,

	SUM(
	IF(
		(condition_of_boundary_wall = 'Satisfactory' OR condition_of_boundary_wall = 'Needs Repair' OR condition_of_boundary_wall = 'Dangerous') and status_detail = 'Functional',
		1,
		0
	)
	) AS boundary_wall,

	SUM(
	IF(
		toilet_facility = 'Yes' and status_detail = 'Functional',
		1,
		0
	)
	) AS Toilet from tabASC tac where docstatus!=2   %s %s )
    
    
    Union  All
    (
    Select "Total",
	SUM(
		CASE WHEN status_detail = "Functional" THEN 1 ELSE 0
	END
	),
	SUM(
		CASE WHEN status_detail = "Closed" THEN 1 ELSE 0
	END
	),
	Count(*),
	
	SUM(
	CASE WHEN tac.school_gender = "Boys" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Boys,
	SUM(
	CASE WHEN tac.school_gender = "Girls" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Girls,
	SUM(
	CASE WHEN tac.school_gender = "Mixed" and status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Mixed,
	SUM(
		CASE WHEN status_detail = "Functional" THEN 1 ELSE 0
	END
	),
	SUM(CASE WHEN total_rooms_school=0  and status_detail= 'Functional' THEN 1 ELSe 0 end) as Shelterless,
	SUM(CASE WHEN status_detail= 'Functional' and total_rooms_school = 1 then 1 else 0 end) as Rooms,



	SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(male_enrollment,0) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(female_enrollment,0) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_enrollment,0) ELSE 0
	END
	),


	SUM(
		CASE WHEN status_detail = "Functional" THEN (coalesce(govt_male_teachers,0) + coalesce(non_govt_male_teachers,0) )  ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN (coalesce(govt_male_teachers,0) + coalesce(non_govt_male_teachers,0)) ELSE 0
	END
	),SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_teacher,0) ELSE 0
	END
	),



	Round( coalesce( (SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_enrollment,0) ELSE 0
	END
	)/SUM(
		CASE WHEN status_detail = "Functional" THEN coalesce(total_teacher,0) ELSE 0
	END
	)
                     ) ,0),0),


	SUM(
	IF(
		water_available = 'Yes' and status_detail= 'Functional' ,
		1,
		0
	)
	)  AS drinking_water,
	SUM(
	IF(
		(electricity_connection = 'WAPDA/KE' OR electricity_connection = 'Solar System') and status_detail = 'Functional',
		1,
		0
	)
	) AS Electricity,

	SUM(
	IF(
		(condition_of_boundary_wall = 'Satisfactory' OR condition_of_boundary_wall = 'Needs Repair' OR condition_of_boundary_wall = 'Dangerous') and status_detail = 'Functional',
		1,
		0
	)
	) AS boundary_wall,

	SUM(
	IF(
		toilet_facility = 'Yes' and status_detail = 'Functional',
		1,
		0
	)
	) AS Toilet from tabASC tac where docstatus!=2   %s )
	 """%(conditions,group_by,conditions)
	data = frappe.db.sql(temp_query,filters)
	return data