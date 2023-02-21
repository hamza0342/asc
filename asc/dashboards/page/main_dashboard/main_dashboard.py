import frappe
@frappe.whitelist()

def get_data(district = None, year = None):
	gender=["Boys","Girls","Mixed"]
	teach_gender=["Male","Female"]
	building=["Katcha","Partially Pakka & katcha","Pakka / RCC / Tier guarder"]
	area=["Urban","Rural"]
	shift=["Morning","Afternoon","Both"]
	building_condition=["Dangerous","Needs Repair","Satisfactory"]
	condition = " and tac.year= '%s' " % str(year)
	if district:
		condition += " and tac.district= '%s' " % str(district)

	get_lvl = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
	case_level = get_level(get_lvl,gender)
	case_shift = get_shift(shift)
	case_type_of_building=get_type_building(building)

	temp_query="""SELECT
	COUNT(tac.name) as total_school,
	SUM(
		CASE WHEN tac.school_gender = "Boys" THEN 1 ELSE 0
	END
	) AS boys,
	SUM(
	CASE WHEN tac.school_gender = "Girls" THEN 1 ELSE 0
	END
	) AS girls,
	SUM(
	CASE WHEN tac.school_gender = "Mixed" THEN 1 ELSE 0
	END
	) AS mixed

	%s    ,

	FORMAT(SUM(tac.non_govt_male_teachers)+SUM(tac.govt_male_teachers),0) male_teachers,
	FORMAT(SUM(tac.non_govt_female_teachers)+SUM(tac.govt_female_teachers),0) female_teachers,
	FORMAT(SUM(tac.total_teacher),0) total_teacher,
	SUM(IF(	water_available = 'Yes',1,0)) AS drinking_water,
	SUM(IF(toilet_facility = "No" OR toilet_facility = "" OR toilet_facility IS NULL,0,1)) AS toilet,
	SUM(IF(electricity_connection = "No Electricity Connection" OR electricity_connection = "" OR electricity_connection IS NULL,0,1)) AS Electricity,
	SUM(IF(condition_of_boundary_wall = "No Boundary Wall" OR condition_of_boundary_wall = "" OR condition_of_boundary_wall IS NULL,0,1)) AS boundary_wall,
	SUM(IF(hand_wash_facility = "No" OR hand_wash_facility = "" OR hand_wash_facility IS NULL,0,1)) AS hand_wash_facility,
	FORMAT(SUM(CASE WHEN tac.wheel_chair_ramp_available="Yes" THEN 1 ELSE 0 END ),0) AS ramp_facility
	%s ,
	SUM(CASE WHEN tac.total_rooms_school=0 THEN 1 ELSE 0 END) as shelterless_school,
	SUM(CASE WHEN tac.total_rooms_school = 1 THEN 1 ELSE 0 END) AS school_with_one_room,
	SUM(CASE WHEN tac.total_rooms_school >1 THEN 1 ELSE 0 END) AS school_with_more_room


	FROM
	tabASC tac
	WHERE tac.docstatus!=2 %s
	""" %(case_shift,case_type_of_building,condition)


	

	#START OF ENROLMENT
	query5="""SELECT 
	FORMAT(SUM(tf.total_class),0)  total_Enrollment,
	SUM(tf.boys)  boys_Enrollment,
	SUM(tf.girls) girls_Enrollment
	FROM
	tabASC tac
	INNER JOIN `tabEnrolment Class and Gender wise` tf ON
	tf.parent = tac.name 
	WHERE tac.docstatus!=2 %s"""%(condition)
	#END of enrolment







	# //Allquery data
	data_ = frappe.db.sql(temp_query, as_dict=1)

	enrolment=frappe.db.sql(query5, as_dict=1)

	Merge(enrolment[0],data_[0])		
 
	#Section for percentages
	data_[0]['boys_percentage'] = round((int(data_[0]['boys']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['girls_percentage'] = round((int(data_[0]['girls']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['mixed_percentage'] = round((int(data_[0]['mixed']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['Morning_percentage'] = round((int(data_[0]['Morning']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['Afternoon_percentage'] = round((int(data_[0]['Afternoon']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['Both_percentage'] = round((int(data_[0]['Both']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['drinking_water_percentage'] = round((int(data_[0]['drinking_water']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['toilet_percentage'] = round((int(data_[0]['toilet']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['electricity_percentage'] = round((int(data_[0]['Electricity']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['hand_wash_facility_percentage'] = round((int(data_[0]['hand_wash_facility']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['boundary_wall_percentage'] = round((int(data_[0]['boundary_wall']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['ramp_facility_percentage'] = round((int(data_[0]['ramp_facility']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['percentage_shelterless_school'] = round((int(data_[0]['shelterless_school']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['percentage_school_with_one_room'] = round((int(data_[0]['school_with_one_room']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['percentage_school_with_more_room'] = round((int(data_[0]['school_with_more_room']) / int(data_[0]['total_school'])) *100,2)


	return data_

def Merge(dict1, dict2):
    return(dict2.update(dict1))

#Dynamic Query
def get_level(level,gender):
	case_string = "" 
	for lvl in level:
		 for gen in gender:
				if lvl=="Higher Secondary":
					lvl1="Higher_Secondary"
				else:
					lvl1=lvl
				case_string += ' , SUM( CASE WHEN tac.school_gender =  "%s" and tac.level= "%s" THEN 1 ELSE 0 END ) AS "%s_%s" ' %(str(gen),str(lvl),str(lvl1),str(gen))
	return case_string	

def get_shift(shift):
	case_string = ""  
	for sh in shift:
		case_string += " , SUM( CASE WHEN tac.shift = '%s' THEN 1 ELSE 0 END ) AS '%s' " %(str(sh),str(sh))
	return case_string	
	

def get_type_building(build):
	case_string = "" 
	for b in build:
			case_string += " , SUM(CASE WHEN tac.type_of_building = '%s' THEN 1 ELSE 0 END )  AS '%s_building' " %(str(b),str(b).split(" ")[0])
	return case_string	


@frappe.whitelist()	
def get_chart_data(district = None, year = None):
    gender=["Boys","Girls","Mixed"]
    condition = " and tac.year= '%s' " % str(year)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    get_lvl = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
    case_level = get_level(get_lvl,gender)
    query8="""SELECT count(tac.name) %s FROM tabASC tac WHERE tac.docstatus!=2 %s"""%(case_level,condition)
    level_gender=frappe.db.sql(query8, as_dict=1)
    return level_gender