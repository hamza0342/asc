import frappe
@frappe.whitelist()

def get_data(district = None, year = None):
	gender=["Boys","Girls","Mixed"]
	teach_gender=["Male","Female"]
	building=["Katcha","Partially Pakka & katcha","Pakka / RCC / Tier guarder"]
	area=["Urban","Rural"]
	shift=["Morning","Afternoon","Both"]
	building_condition=["Dangerous","Needs Repair","Satisfactory"]
	teacher_desig=["DT","ECT","HM","HST","JST/JEST","Non-Government","Other","PST","PTI","SST","WIT"]
	condition = " and tac.year= '%s' " % str(year)
	if district:
		condition += " and tac.district= '%s' " % str(district)

	get_lvl = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
	case_level = get_level(get_lvl,gender)
	case_shift = get_shift(shift)
	case_shift_gender = get_shift_gender(shift,gender)
	case_type_of_building=get_type_building(building)
	case_location_gender=get_location_gender(area,gender)
	case_enrol_medium=get_medium_enrol(get_lvl)
	case_building_condition=get_building_condition(get_lvl,building_condition)
	case_building_Rented_Other=get_building_Rented_Other(get_lvl)
	case_no_building=get_no_building(get_lvl)
	case_teacher_designation=get_teacher_designation(teacher_desig,teach_gender)

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
	) AS mixed,
	SUM(CASE WHEN tac.level = 'Primary' THEN 1 ELSE 0 END) As primary_schools,
	SUM(CASE WHEN tac.level = 'Middle' THEN 1 ELSE 0 END) As middle_schools,
	SUM(CASE WHEN tac.level = 'Elementary' THEN 1 ELSE 0 END) As elem_schools,
	SUM(CASE WHEN tac.level = 'Secondary' THEN 1 ELSE 0 END) As secondary_schools,
	SUM(CASE WHEN tac.level = 'Higher Secondary' THEN 1 ELSE 0 END) As high_sec_schools

	%s  %s %s %s %s ,
	SUM(CASE WHEN  (tac.no_relevant_code = "tree" OR tac.no_relevant_code = "chappra" OR tac.no_relevant_code = "hut" or condition_of_building IS NULL OR total_rooms_school = 0) AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END )      AS Middle_Elementary_No_Building,
	ROUND(SUM(CASE WHEN  (tac.no_relevant_code = "tree" OR tac.no_relevant_code = "chappra" OR tac.no_relevant_code = "hut") AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END )/SUM(CASE WHEN tac.level = "Middle" OR tac.level="Elementary" THEN 1 ELSE 0 END)*100,2) as Middle_Elementary_No_Building_percentage,
	SUM(CASE WHEN  (tac.yes_relevant_code = "Rented" OR tac.yes_relevant_code = "Others" ) AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END )      AS Middle_Elementary_Rented_Others,
	ROUND(SUM(CASE WHEN  (tac.yes_relevant_code = "Rented" OR tac.yes_relevant_code = "Others" ) AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END )/SUM(CASE WHEN tac.level = "Primary" THEN 1 ELSE 0 END)*100,2) as Middle_Elementary_Rented_Others_percentage,
	SUM(CASE WHEN  availability_of_building = 'Yes' AND condition_of_building = 'Satisfactory' AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END ) AS Middle_Elementary_Satisfactory,
	SUM(CASE WHEN availability_of_building = 'Yes' AND condition_of_building = 'Needs Repair' AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END ) AS Middle_Elementary_Needs_Repair,
	SUM(CASE WHEN availability_of_building = 'Yes' AND condition_of_building = 'Dangerous'  AND (tac.level = "Middle" OR tac.level="Elementary") THEN 1 ELSE 0 END ) AS Middle_Elementary_Dangerous,
	SUM(CASE WHEN tac.status_detail = "Functional" THEN 1 ELSE 0 END) as functional_schools,
	SUM(CASE WHEN tac.status_detail = "Closed" THEN 1 ELSE 0 END ) as non_functional_schools,
	SUM(CASE WHEN tac.location="Urban" then 1 else 0 end) as urban,
	SUM(CASE WHEN tac.location="Rural" then 1 else 0 end) as rural,
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
	SUM(CASE WHEN tac.total_rooms_school >1 THEN 1 ELSE 0 END) AS school_with_more_room,
	SUM(CASE WHEN tac.internet_connection != "Not Available" Then 1 else 0 END) as internet,
	SUM(CASE WHEN tac.computer_lab != "Not Available" Then 1 else 0 END) as computer,
	SUM(CASE WHEN tac.science_lab != "Not Available" Then 1 else 0 END) as science,
	SUM(CASE WHEN tac.chemistry_lab != "Not Available" Then 1 else 0 END) as chemistry,
 	SUM(CASE WHEN tac.physics_lab != "Not Available" Then 1 else 0 END) as physics,
 	SUM(CASE WHEN tac.biology_lab != "Not Available" Then 1 else 0 END) as biology,
 	SUM(CASE WHEN tac.home_economics_lab != "Not Available" Then 1 else 0 END) as homeeconomics,
	SUM(CASE WHEN tac.library != "Not Available" Then 1 else 0 END) as library,
   	SUM(CASE WHEN tac.play_ground_available = 1 Then 1 else 0 END) as play_gound,
 	SUM(CASE WHEN tac.medical__first_aid_box != "Not Available" Then 1 else 0 END) as medical_aid_box,
	SUM(polio_affected + physical_disabilites) as special_students,
	SUM(CASE WHEN tac.level = 'Elementry' OR tac.level = 'Middle' THEN 1 ELSE 0 END) as total_elementry


	FROM
	tabASC tac
	WHERE tac.docstatus!=2 %s
	""" %(case_shift,case_shift_gender,case_building_condition,case_building_Rented_Other,case_no_building,case_type_of_building,condition)


 
	# Student Teacher Ratio
	st_ratio_query= """Select  SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) as total_student,
	SUM(tac.total_teacher) AS total_Teacher,
 
	SUM(CASE WHEN level = 'Primary' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END) as total_primary_student,
 	SUM(CASE WHEN level = 'Primary' THEN (total_teacher) ELSE 0 END) as total_primary_teacher,

	SUM(CASE WHEN level = 'Elementary' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END) as total_elementary_student,
 	SUM(CASE WHEN level = 'Elementary' THEN (total_teacher) ELSE 0 END) as total_elementary_teacher,

	SUM(CASE WHEN level = 'Middle' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END) as total_middle_student,
 	SUM(CASE WHEN level = 'Middle' THEN (total_teacher) ELSE 0 END) as total_middle_teacher,

	SUM(CASE WHEN level = 'Secondary' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END) as total_secondary_student,
 	SUM(CASE WHEN level = 'Secondary' THEN (total_teacher) ELSE 0 END) as total_secondary_teacher,

	SUM(CASE WHEN level = 'Higher Secondary' THEN (sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) ELSE 0 END) as total_higher_secondary_student,
 	SUM(CASE WHEN level = 'Higher Secondary' THEN (total_teacher) ELSE 0 END) as total_higher_secondary_teacher
	FROM tabASC tac where docstatus!=2 %s
	"""%(condition)
	# END of Student Teacher Ratio

	#Student School Ratio
	ss_ratio_query = """SELECT
 	SUM(CASE WHEN level = 'Primary' THEN 1 ELSE 0 END) as total_primary_school,

 	SUM(CASE WHEN level = 'Elementary' THEN 1 ELSE 0 END) as total_elementary_school,

 	SUM(CASE WHEN level = 'Middle' THEN 1 ELSE 0 END) as total_middle_school,

 	SUM(CASE WHEN level = 'Secondary' THEN 1 ELSE 0 END) as total_secondary_school,

 	SUM(CASE WHEN level = 'Higher Secondary' THEN 1 ELSE 0 END) as total_higher_secondary_school
	FROM tabASC tac where docstatus!=2 %s
	"""%(condition)
	#Student School Ratio
 
	#Student Classroom Ratio
	sc_ratio_query ="""SELECT
	SUM(total_rooms) as total_classroom,

 	SUM(CASE WHEN level = 'Primary' THEN total_rooms ELSE 0 END) as total_primary_classroom,

 	SUM(CASE WHEN level = 'Elementary' THEN total_rooms ELSE 0 END) as total_elementary_classroom,

 	SUM(CASE WHEN level = 'Middle' THEN total_rooms ELSE 0 END) as total_middle_classroom,

 	SUM(CASE WHEN level = 'Secondary' THEN total_rooms ELSE 0 END) as total_secondary_classroom,

 	SUM(CASE WHEN level = 'Higher Secondary' THEN total_rooms ELSE 0 END) as total_higher_secondary_classroom
	FROM tabASC tac where docstatus!=2 %s
	"""%(condition)
	# END of Student Classroom ratio
	

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


	#start of teacher chart
	query10="""SELECT COUNT(gender) %s 
	FROM
	 `tabWorking Teaching Staff Detail` AS teach
	 INNER JOIN tabASC tac ON tac.name=teach.asc
	where teach.docstatus!=2 and tac.docstatus!=2 %s
	"""%(case_teacher_designation,condition)
	#end of teacher chart
	papulation = None
	if district:
		papulation_query = "Select overall_papulation FROM `tabDistrict Population` where parent= '%s' and year = '%s' "%(str(district),str(year))
		papulation =frappe.db.sql(papulation_query)
	else:
		papulation_query = "Select SUM(overall_papulation) FROM `tabDistrict Population` where  year = '%s' "%(str(year))
		papulation =frappe.db.sql(papulation_query)




	# //Allquery data
	data_ = frappe.db.sql(temp_query, as_dict=1)
	data_[0]['papulation'] = 0
	if papulation:
		data_[0]['papulation'] = papulation[0]
	fun_non_fun={
		'functional_percentage' : 0 ,
        'non_functional_percentage': 0
	}

	teacher_ratio=frappe.db.sql(st_ratio_query, as_dict=1)
	school_ratio=frappe.db.sql(ss_ratio_query, as_dict=1)
	classroom_ratio=frappe.db.sql(sc_ratio_query, as_dict=1)
	enrolment=frappe.db.sql(query5, as_dict=1)
	desig=frappe.db.sql(query10, as_dict=1)
	data_.append(fun_non_fun)
	data_.append(desig)

	Merge(teacher_ratio[0],data_[0])
	Merge(school_ratio[0],data_[0])
	Merge(classroom_ratio[0],data_[0])
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
	data_[1]['functional_percentage'] = round((int(data_[0]['functional_schools'])/int(data_[0]['total_school'])) *100 , 0)
	data_[1]['non_functional_percentage'] = round((int(data_[0]['non_functional_schools']) / int(data_[0]['total_school'])) *100 , 0)
	data_[0]['urban_percentage'] = round((int(data_[0]['urban']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['rural_percentage'] = round((int(data_[0]['rural']) / int(data_[0]['total_school'])) *100,2)
	data_[0]['enrol_percentage'] = 0
	data_[0]['g_percentage'] = 0
	data_[0]['b_percentage'] = 0
	data_[0]['s_percentage'] = 0
	data_[0]['un_percentage'] = 0
	if papulation:
		if papulation[0][0]:
			data_[0]['enrol_percentage'] = round((int(data_[0]['boys_Enrollment'])+ int(data_[0]['girls_Enrollment'])) / (papulation[0][0]) *100 ,1 )
			data_[0]['g_percentage'] = round((int(data_[0]['girls_Enrollment'])) / (papulation[0][0]) *100 ,1 ) 
			data_[0]['b_percentage'] = round((int(data_[0]['boys_Enrollment'])) / (papulation[0][0]) *100 ,1 )
			data_[0]['s_percentage'] = round((int(data_[0]['special_students'])) / (papulation[0][0]) *100 ,1 )
			data_[0]['un_percentage'] = round(( int(papulation[0][0]) - (int(data_[0]['boys_Enrollment'])+ int(data_[0]['girls_Enrollment']))) / (papulation[0][0]) *100 ,1 ) 
		else:
			data_[0]['enrol_percentage'] = 0
			data_[0]['g_percentage'] = 0
			data_[0]['b_percentage'] = 0
			data_[0]['s_percentage'] = 0
			data_[0]['un_percentage'] = 0


	# Building Table Percentages
	data_[0]['Primary_Satisfactory_percentage'] = round((int(data_[0]['Primary_Satisfactory']) / int(data_[0]['primary_schools'])) *100,2)
	data_[0]['Primary_Needs_Repair_percentage'] = round((int(data_[0]['Primary_Needs_Repair']) / int(data_[0]['primary_schools'])) *100,2)
	data_[0]['Primary_Dangerous_percentage'] = round((int(data_[0]['Primary_Dangerous']) / int(data_[0]['primary_schools'])) *100,2)
	data_[0]['Primary_Rented_Others_percentage'] = round((int(data_[0]['Primary_Rented_Others']) / int(data_[0]['primary_schools'])) *100,2)
	
 
	data_[0]['Middle_Elementary_Satisfactory_percentage'] = round((int(data_[0]['Middle_Elementary_Satisfactory']) / int(data_[0]['total_elementry'])) *100,2)
	data_[0]['Middle_Elementary_Needs_Repair_percentage'] = round((int(data_[0]['Middle_Elementary_Needs_Repair']) / int(data_[0]['total_elementry'])) *100,2)
	data_[0]['Middle_Elementary_Dangerous_percentage'] = round((int(data_[0]['Middle_Elementary_Dangerous']) / int(data_[0]['total_elementry'])) *100,2)
	data_[0]['Middle_Elementary_Rented_Others_percentage'] = round((int(data_[0]['Middle_Elementary_Rented_Others']) / int(data_[0]['total_elementry'])) *100,2)


	data_[0]['Secondary_Satisfactory_percentage'] = round((int(data_[0]['Secondary_Satisfactory']) / int(data_[0]['secondary_schools'])) *100,2)
	data_[0]['Secondary_Needs_Repair_percentage'] = round((int(data_[0]['Secondary_Needs_Repair']) / int(data_[0]['secondary_schools'])) *100,2)
	data_[0]['Secondary_Dangerous_percentage'] = round((int(data_[0]['Secondary_Dangerous']) / int(data_[0]['secondary_schools'])) *100,2)
	data_[0]['Secondary_Rented_Others_percentage'] = round((int(data_[0]['Secondary_Rented_Others']) / int(data_[0]['secondary_schools'])) *100,2)
 
 

	data_[0]['Higher_Secondary_Satisfactory_percentage'] = round((int(data_[0]['Higher_Secondary_Satisfactory']) / int(data_[0]['high_sec_schools'])) *100,2)
	data_[0]['Higher_Secondary_Needs_Repair_percentage'] = round((int(data_[0]['Higher_Secondary_Needs_Repair']) / int(data_[0]['high_sec_schools'])) *100,2)
	data_[0]['Higher_Secondary_Dangerous_percentage'] = round((int(data_[0]['Higher_Secondary_Dangerous']) / int(data_[0]['high_sec_schools'])) *100,2)
	data_[0]['Higher_Secondary_Rented_Others_percentage'] = round((int(data_[0]['Higher_Secondary_Rented_Others']) / int(data_[0]['high_sec_schools'])) *100,2)
 

	#End of Percentage section
	
	#Calulation of Ratios
	data_[0]['Students_Per_Teacher']= round(int(data_[0]['total_student']) / int(data_[0]['total_Teacher']),0)
	data_[0]['primary_teacher_per_student']= round(int(data_[0]['total_primary_student']) / int(data_[0]['total_primary_teacher']),0)
	# data_[0]['elementary_teacher_per_student']= round(int(data_[0]['total_elementary_student']) / int(data_[0]['total_elementary_teacher']),0)
	data_[0]['elementary_teacher_per_student']= round(int(data_[0]['total_elementary_student']) / 1,0)
	data_[0]['secondary_teacher_per_student']= round(int(data_[0]['total_secondary_student']) / int(data_[0]['total_secondary_teacher']),0)
	data_[0]['middle_teacher_per_student']= round(int(data_[0]['total_middle_student']) / int(data_[0]['total_middle_teacher']),0)
	data_[0]['higher_secondary_teacher_per_student']= round(int(data_[0]['total_higher_secondary_student']) / int(data_[0]['total_higher_secondary_teacher']),0)
	data_[0]['Students_Per_School']= round(int(data_[0]['total_student']) / int(data_[0]['total_school']),0)
	data_[0]['primary_student_per_teacher']= round(int(data_[0]['total_primary_student']) / int(data_[0]['total_primary_school']),0)
	data_[0]['elementary_student_per_school']= round(int(data_[0]['total_elementary_student']) / int(data_[0]['total_elementary_school']),0)
	data_[0]['middle_student_per_school']= round(int(data_[0]['total_middle_student']) / int(data_[0]['total_middle_school']),0)
	data_[0]['secondary_student_per_school']= round(int(data_[0]['total_secondary_student']) / int(data_[0]['total_secondary_school']),0)
	data_[0]['higher_secondary_student_per_school']= round(int(data_[0]['total_higher_secondary_student']) / int(data_[0]['total_higher_secondary_school']),0)
	data_[0]['student_per_classroom']= round(int(data_[0]['total_student']) / int(data_[0]['total_classroom']),0)
	data_[0]['primary_per_student_classroom']= round(int(data_[0]['total_primary_student']) / int(data_[0]['total_primary_classroom']),0)
	data_[0]['elementary_per_student_classroom']= round(int(data_[0]['total_elementary_student']) / int(data_[0]['total_elementary_classroom']),0)
	data_[0]['middle_per_student_classroom']= round(int(data_[0]['total_middle_student']) / int(data_[0]['total_middle_classroom']),0)
	data_[0]['secondary_per_student_classroom']= round(int(data_[0]['total_secondary_student']) / int(data_[0]['total_secondary_classroom']),0)
	data_[0]['higher_secondary_per_student_classroom']= round(int(data_[0]['total_higher_secondary_student']) / int(data_[0]['total_higher_secondary_classroom']),0)



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


def get_shift_gender(shift,gender):
	case_string = "" 
	for sh in shift:
		for gen in gender:
			case_string += " , SUM( CASE WHEN tac.shift = '%s' and tac.school_gender= '%s' THEN 1 ELSE 0 END )  AS '%s_%s' " %(str(sh),str(gen),str(sh),str(gen))
	return case_string	

def get_type_building(build):
	case_string = "" 
	for b in build:
			case_string += " , SUM(CASE WHEN tac.type_of_building = '%s' THEN 1 ELSE 0 END )  AS '%s_building' " %(str(b),str(b).split(" ")[0])
	return case_string	


def get_location_gender(area,gender):
	case_string = "" 
	for a in area:
		for g in gender:
			case_string += "  ,SUM(CASE WHEN tac.location= '%s' and tac.school_gender= '%s' THEN 1 ELSE 0 END)  AS '%s_%s' ," %(str(a),str(g),str(a),str(g))
			case_string += " ROUND(SUM(CASE WHEN tac.location='%s' and tac.school_gender='%s' THEN 1 ELSE 0 END ) / SUM(CASE WHEN tac.location='%s' then 1 else 0 end) * 100,0)  AS '%s_%s_percentage' " %(str(a),str(g),str(a),str(a),str(g))
	return case_string	
def get_medium_enrol(level):
	case_string=""
	for l in level:
		if l=="Higher Secondary":
			l1="Higher_Secondary"
		else:
			l1=l
		case_string+=""",
			SUM(
				CASE 
				WHEN urdu_medium_enrolment>0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment=0 AND tac.level='%s' THEN 1
				ELSE 0
				END
				) AS '%s_urdu_enrol',
				SUM(
					CASE 
				WHEN urdu_medium_enrolment=0 AND english_medium_enrolment>0 AND sindhi_medium_enrolment=0 AND tac.level='%s' THEN 1
				ELSE 0
				END
				)  AS '%s_english_enrol',
				SUM(
					CASE 
				WHEN urdu_medium_enrolment=0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment>0 AND tac.level='%s' THEN 1
				ELSE 0
				END
				) AS '%s_sindth_enrol',
				SUM(
					CASE
					WHEN sindhi_medium_enrolment>0 AND urdu_medium_enrolment>0 AND tac.level='%s' THEN 1
					WHEN sindhi_medium_enrolment>0 AND english_medium_enrolment>0 AND tac.level='%s' THEN 1
					WHEN urdu_medium_enrolment>0 AND english_medium_enrolment>0 AND tac.level='%s'  THEN 1
					WHEN urdu_medium_enrolment>0 AND english_medium_enrolment>0 AND sindhi_medium_enrolment>0 AND tac.level='%s'  THEN 1
					ELSE 0
					END
				) AS '%s_mixed_enrol' """%(l,l1,l,l1,l,l1,l,l,l,l,l1)
			
	return case_string


def get_building_condition(level,building):
	case_string = "" 
	for lvl in level:
		 for b in building:

				if b=="Needs Repair":
					bb="Needs_Repair"
				else:
					bb=b
				if lvl=="Higher Secondary":
					lvl1="Higher_Secondary"
				else:
					lvl1=lvl
				if(lvl!="Middle" and lvl!="Elementary"):	
					case_string += """
						, SUM(CASE WHEN tac.condition_of_building=  '%s' and tac.level = '%s'
						THEN 1 ELSE 0 END) AS '%s_%s'  """ %(
							str(b),str(lvl),str(lvl1),str(bb))
	return case_string	

def get_building_Rented_Other(level):
	case_string = ""
	lvl1 = ""
	for lvl in level:
			if lvl=="Higher Secondary":
				lvl1="Higher_Secondary"
			else:
				lvl1=lvl
			if(lvl!="Middle" and lvl!="Elementary"):	
				case_string += """
					, SUM(CASE WHEN tac.level = '%s'and (tac.yes_relevant_code = "Rented" OR tac.yes_relevant_code = "Other" )
					THEN 1 ELSE 0 END) AS '%s_Rented_Others'  """ %(
						str(lvl),str(lvl1))
	return case_string	

def get_no_building(level):
	case_string = ""
	lvl1=""
	for lvl in level:
			if lvl=="Higher Secondary":
				lvl1="Higher_Secondary"
			else:
				lvl1=lvl
			if(lvl!="Middle" and lvl!="Elementary"):	
				case_string += """
					, 
					SUM(CASE WHEN tac.level = '%s' and (tac.no_relevant_code = "tree" OR tac.no_relevant_code = "chappra" OR tac.no_relevant_code = "hut" OR condition_of_building IS NULL OR total_rooms_school = 0 OR availability_of_building = 'No' )
					THEN 1 ELSE 0 END) AS '%s_No_Building' , 
					Round(SUM(CASE WHEN tac.level = '%s'and (tac.no_relevant_code = "tree" OR tac.no_relevant_code = "chappra" OR tac.no_relevant_code = "hut" OR condition_of_building IS NULL OR total_rooms_school = 0 OR availability_of_building ='No')
					THEN 1 ELSE 0 END)/SUM(CASE WHEN tac.level = '%s' THEN 1 ELSE 0 END) *100 ,2)AS '%s_No_Building_Percentage' """ %(
						str(lvl),str(lvl1),str(lvl),str(lvl),str(lvl1))
	return case_string	

def get_teacher_designation(desig,gender):
	case_string=""
	for g in gender:
		for d in desig:
			case_string+=", SUM(CASE WHEN teach.designation_code='%s' and teach.gender='%s' THEN 1 ELSE 0 END) AS '%s_%s'"%(str(d),str(g),str(g),str(d))
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

@frappe.whitelist()	
def get_enrollment_data(district = None, year = None):
    condition = " and tac.year= '%s' " % str(year)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    query9="""SELECT tabProgram.profile_order As "order", 
	SUM(enrol.boys) AS boys,
	SUM(enrol.girls) AS girls
	FROM `tabEnrolment Class and Gender wise` enrol
	CROSS join tabProgram on enrol.class = tabProgram.name 
	LEFT JOIN tabASC tac on enrol.parent = tac.name
	WHERE tac.docstatus!=2 %s
	Group By tabProgram.profile_order
	ORDER BY tabProgram.profile_order"""%condition
    enrollment=frappe.db.sql(query9, as_dict=1)
    return enrollment


@frappe.whitelist()	
def location_gender_schools(district = None, year = None):
    condition = " and tac.year= '%s' " % str(year)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    area=["Urban","Rural"]
    gender=["Boys","Girls","Mixed"]
    case_location_gender=get_location_gender(area,gender)
    location_wise_schools="""Select COUNT(tac.name) %s FROM tabASC tac WHERE tac.docstatus!=2 %s"""%(case_location_gender,condition)
    enrollment=frappe.db.sql(location_wise_schools, as_dict=1)
    return enrollment

@frappe.whitelist()	
def medium_level_schools(district = None, year = None):
    condition = " and tac.year= '%s' " % str(year)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    get_lvl = frappe.db.get_list('Level', pluck='name', order_by='list_order asc')
    case_enrol_medium=get_medium_enrol(get_lvl)
    medium_wise_schools="""Select count(tac.name) %s FROM tabASC tac WHERE tac.docstatus!=2 %s"""%(case_enrol_medium,condition)
    data=frappe.db.sql(medium_wise_schools, as_dict=1)
    return data

@frappe.whitelist()	
def teachers_data(district = None, year = None):
    condition = " and tac.year= '%s' " % str(year)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    teacher_desig=["DT","ECT","HM","HST","JST/JEST","Non-Government","Other","PST","PTI","SST","WIT"]
    teach_gender=["Male","Female"]
    case_teacher_designation=get_teacher_designation(teacher_desig,teach_gender)
    teacher_query="""SELECT COUNT(gender) %s FROM `tabWorking Teaching Staff Detail` AS teach INNER JOIN tabASC tac ON tac.name=teach.asc where teach.docstatus!=2 and tac.docstatus!=2 %s"""%(case_teacher_designation,condition)
    data=frappe.db.sql(teacher_query, as_dict=1)
    return data