import frappe
@frappe.whitelist()

def get_data(year = None):
    condition = ""
    if year:
        condition += " and year= '%s' " % str(year)
    else:
        condition = " and year= '2021-22' " 
    temp_query=""" SELECT year,
    COUNT(name) as total_school,
    SUM(Case when status_detail = "Functional" Then 1 else 0 end) as functional,
    SUM(Case when status_detail = "Closed" Then 1 else 0 end) as closed,
    SUM(CASE WHEN school_gender = "Boys" THEN 1 ELSE 0 END ) AS boys,
 	SUM(CASE WHEN school_gender = "Girls" THEN 1 ELSE 0 END ) AS girls,
	SUM( CASE WHEN school_gender = "Mixed" THEN 1 ELSE 0 END ) AS mixed,

    SUM(CASE when shift = 'Morning' and school_gender = 'Boys' Then 1 else 0 end) AS morning_boys,
    SUM(CASE when shift = 'Morning' and school_gender = 'Girls' Then 1 else 0 end) AS morning_girls,
    SUM(CASE when shift = 'Morning' and school_gender = 'Mixed' Then 1 else 0 end) AS morning_mixed,

    SUM(CASE when shift = 'Afternoon' and school_gender = 'Boys' Then 1 else 0 end) AS Afternoon_boys,
    SUM(CASE when shift = 'Afternoon' and school_gender = 'Girls' Then 1 else 0 end) AS Afternoon_girls,
    SUM(CASE when shift = 'Afternoon' and school_gender = 'Mixed' Then 1 else 0 end) AS Afternoon_mixed,

    SUM(CASE when shift = 'Both' and school_gender = 'Boys' Then 1 else 0 end) AS Both_boys,
    SUM(CASE when shift = 'Both' and school_gender = 'Girls' Then 1 else 0 end) AS Both_girls,
    SUM(CASE when shift = 'Both' and school_gender = 'Mixed' Then 1 else 0 end) AS Both_mixed,

    SUM(
		CASE WHEN major_reason_closure = "Non availability of Teacher" THEN 1 ELSE 0
	END
	) AS no_teacher,
	SUM(
		CASE WHEN major_reason_closure = "No Enrollment" or major_reason_closure = "No Population / No Enrollment" THEN 1 ELSE 0
	END
	) AS no_enrollment,
    SUM(
		CASE WHEN major_reason_closure = "School does not exist" or major_reason_closure = "Due to litigation" 
		or major_reason_closure = "School ceases to function long time ago and no record available for this school (Not in existence)"
		or major_reason_closure = 'No Population' or major_reason_closure = 'Any Other'  or major_reason_closure ='Due to Law-and-order situation of area'
		THEN 1 ELSE 0 
	END
	) AS other_closure_reason,


	SUM(IF(	water_available = 'Yes',1,0)) AS drinking_water,
	SUM(IF(condition_of_boundary_wall = "No Boundary Wall" OR condition_of_boundary_wall = "" OR condition_of_boundary_wall IS NULL,0,1)) AS boundary_wall,
 	SUM(IF(electricity_connection = "No Electricity Connection" OR electricity_connection = "" OR electricity_connection IS NULL,0,1)) AS Electricity,
  	SUM(IF(hand_wash_facility = "No" OR hand_wash_facility = "" OR hand_wash_facility IS NULL,0,1)) AS hand_wash_facility,
   	SUM(IF(toilet_facility = "No" OR toilet_facility = "" OR toilet_facility IS NULL,0,1)) AS toilet,
    SUM(CASE WHEN wheel_chair_ramp_available="Yes" THEN 1 ELSE 0 END ) AS ramp_facility,
    SUM( CASE WHEN shift = 'Morning' THEN 1 ELSE 0 END ) AS morning,
    SUM( CASE WHEN shift = 'Afternoon' THEN 1 ELSE 0 END ) AS afternoon,
    SUM( CASE WHEN shift = 'Both' THEN 1 ELSE 0 END ) AS both_ ,
    SUM(CASE WHEN availability_of_building = "No" THEN 1 ELSE 0 END) as shelterless_school,
    SUM(CASE WHEN availability_of_building = "Yes" THEN 1 ELSE 0 END) AS sheltered_school,
    SUM(non_govt_female_teachers)+SUM(govt_female_teachers) as female_teachers,
    SUM(non_govt_male_teachers)+SUM(govt_male_teachers) male_teachers,
    SUM(male_enrollment) boys_Enrollment,
    SUM(female_enrollment) girls_Enrollment
 
    from tabASC where docstatus != 2 %s
    """%(condition)
    # frappe.msgprint(temp_query)
    data_ = frappe.db.sql(temp_query, as_dict=1)

    
    data_[0]['boys_percentage'] = round((int(data_[0]['boys']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['girls_percentage'] = round((int(data_[0]['girls']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['mixed_percentage'] = round((int(data_[0]['mixed']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['Morning_percentage'] = round((int(data_[0]['morning']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['Afternoon_percentage'] = round((int(data_[0]['afternoon']) / int(data_[0]['total_school'])) *100,2) 
    data_[0]['Sheltered_percentage'] = round((int(data_[0]['sheltered_school']) / int(data_[0]['total_school'])) *100,2) 
    data_[0]['Shelterless_percentage'] = round((int(data_[0]['shelterless_school']) / int(data_[0]['total_school'])) *100,2) 
    data_[0]['closed_percentage'] = round((int(data_[0]['closed']) / int(data_[0]['total_school'])) *100,2) 
    data_[0]['functional_percentage'] = round((int(data_[0]['functional']) / int(data_[0]['total_school'])) *100,2) 
    
    data_[0]['Both_percentage'] = round((int(data_[0]['both_']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['drinking_water_percentage'] = round((int(data_[0]['drinking_water']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['toilet_percentage'] = round((int(data_[0]['toilet']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['electricity_percentage'] = round((int(data_[0]['Electricity']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['hand_wash_facility_percentage'] = round((int(data_[0]['hand_wash_facility']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['boundary_wall_percentage'] = round((int(data_[0]['boundary_wall']) / int(data_[0]['total_school'])) *100,2)
    data_[0]['ramp_facility_percentage'] = round((int(data_[0]['ramp_facility']) / int(data_[0]['total_school'])) *100,2)
    if data_[0]['no_teacher'] :
        data_[0]['no_teacher_percentage'] = round(data_[0]['no_teacher'] / data_[0]['closed'] * 100, 1)
    else:
        data_[0]['no_teacher_percentage'] = 0
    if data_[0]['no_enrollment'] :
        data_[0]['no_enrollment_percentage'] = round(data_[0]['no_enrollment'] / data_[0]['closed'] * 100, 1)
    else:
        data_[0]['no_enrollment_percentage'] = 0
    if data_[0]['other_closure_reason'] :
        data_[0]['other_closure_reason_percentage'] = round(data_[0]['other_closure_reason'] /data_[0]['closed'] * 100, 1)
    else:
        data_[0]['other_closure_reason_percentage'] = 0
    user_role = 0
    get_semis_role = frappe.db.get_value("User", frappe.session.user, "semis_manager")
    if get_semis_role:
        user_role = 1
    data_[0]['user_roles'] = user_role
    return data_
    


 
	#Section for percentages
	# data_[0]['Morning_percentage'] = round((int(data_[0]['Morning']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['Afternoon_percentage'] = round((int(data_[0]['Afternoon']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['Both_percentage'] = round((int(data_[0]['Both']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['drinking_water_percentage'] = round((int(data_[0]['drinking_water']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['toilet_percentage'] = round((int(data_[0]['toilet']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['electricity_percentage'] = round((int(data_[0]['Electricity']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['hand_wash_facility_percentage'] = round((int(data_[0]['hand_wash_facility']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['boundary_wall_percentage'] = round((int(data_[0]['boundary_wall']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['ramp_facility_percentage'] = round((int(data_[0]['ramp_facility']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['percentage_shelterless_school'] = round((int(data_[0]['shelterless_school']) / int(data_[0]['total_school'])) *100,2)
	# data_[0]['sheltered_school_percentage'] = round((int(data_[0]['sheltered_school']) / int(data_[0]['total_school'])) *100,2)


def Merge(dict1, dict2):
    return(dict2.update(dict1))

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


@frappe.whitelist()	
def get_role(district = None, year = None):
    user_role = 0
    get_semis_role = frappe.db.get_value("User", frappe.session.user, "semis_manager")
    if get_semis_role:
        user_role = 1
    return user_role