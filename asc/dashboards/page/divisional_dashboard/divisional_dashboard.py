import frappe
import re


@frappe.whitelist()
def get_data(district=None, year=None):
	condition = " and tac.year= '%s' " % str(year)
	if district:
		condition += " and tac.region= '%s' " % str(district)

	temp_query = """SELECT
	year,
	region as district,
	year,
	COUNT(DISTINCT tac.name)  AS Total_Schools,
	SUM(total_enrollment) AS Enrolments,
	
	SUM(govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) AS Teachers,
	SUM(
		CASE WHEN tac.status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Functional,
	SUM(
		CASE WHEN tac.status_detail = "Closed" THEN 1 ELSE 0
	END
	) AS Closed,
	SUM(
		CASE WHEN tac.major_reason_closure = "Non availability of Teacher" THEN 1 ELSE 0
	END
	) AS no_teacher,
	SUM(
		CASE WHEN tac.major_reason_closure = "No Enrollment" or tac.school_duration_of_closure = "No Population / No Enrollment" THEN 1 ELSE 0
	END
	) AS no_enrollment,
	SUM(
		CASE WHEN tac.major_reason_closure = "School does not exist" or tac.school_duration_of_closure = "Due to litigation" 
		or tac.school_duration_of_closure = "School ceases to function long time ago and no record available for this school (Not in existence)"
		or tac.major_reason_closure = 'No Population' or tac.major_reason_closure = 'Any Other'
		THEN 1 ELSE 0 
	END
	) AS other_closure_reason,
	SUM(
	CASE WHEN tac.school_gender = "Boys" THEN 1 ELSE 0
	END
	) AS Boys,
	SUM(
	CASE WHEN tac.school_gender = "Girls" THEN 1 ELSE 0
	END
	) AS Girls,
	SUM(
	CASE WHEN tac.school_gender = "Mixed" THEN 1 ELSE 0
	END
	) AS Mixed,
	SUM(
	CASE WHEN tac.level = "Elementary" THEN 1 ELSE 0
	END
	) AS Elementary,
	SUM(
	CASE WHEN tac.level = "Primary" THEN 1 ELSE 0
	END
	) AS primary_school,
	SUM(
	CASE WHEN tac.level = "Middle" THEN 1 ELSE 0
	END
	) AS Middle,
	SUM(
	CASE WHEN tac.level = "Secondary" THEN 1 ELSE 0
	END
	) AS Secondary,
	SUM(
	CASE WHEN tac.level = "Higher Secondary" THEN 1 ELSE 0
	END
	) AS higher_secondary,
	
	SUM(
	IF(
		(condition_of_boundary_wall = 'Satisfactory' OR condition_of_boundary_wall = 'Needs Repair' OR condition_of_boundary_wall = 'Dangerous') and status_detail = 'Functional',
		1,
		0
	)
	) AS boundary_wall,
	
	
	SUM(
	CASE WHEN tac.is_this_branch_school = "Yes" THEN 1 ELSE 0
	END
	) AS Branch,
	SUM(
	CASE WHEN tac.adopted_school = "Yes" THEN 1 ELSE 0
	END
	) AS adopted_school,
	SUM(
	IF(
	toilet_facility = 'Yes' and status_detail = 'Functional',
	1,
	0
	)
	) AS Toilet,
	SUM(
	CASE WHEN tac.is_campus_school = "yes" THEN 1 ELSE 0
	END
	) AS Campus,
	SUM(CASE WHEN tac.total_rooms_school=0  and status_detail= 'Functional' THEN 1 ELSe 0 end) as Shelterless,
	SUM(CASE WHEN tac.availability_of_building='Yes' and status_detail = 'Functional' THEN 1 ELSe 0 end) as having_building,
	SUM(CASE WHEN status_detail= 'Functional' then total_rooms_school else 0 end) as Rooms,
	SUM(CASE WHEN status_detail= 'Functional' then total_rooms else 0 end) as Classrooms,
	SUM(CASE WHEN total_rooms_school>0 THEN 1 ELSE 0 END) as Rooms_school,
	SUM(CASE WHEN total_rooms >0 THEN 1 ELSE 0 END) as Classrooms_school,

	

	CURDATE() AS date_
	FROM
	tabASC tac WHERE tac.docstatus!=2 %s""" % (condition)

	data_ = frappe.db.sql(temp_query, as_dict=1)
	if not data_:
		return 1

	if data_[0]['Total_Schools']:
		if data_[0]['Functional']:
			data_[0]['func_percentage'] = round(data_[0]['Functional'] / data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['func_percentage'] = 0
		if data_[0]['Closed']:
			data_[0]['closed_percentage'] = round(data_[0]['Closed'] / data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['closed_percentage'] = 0
		if data_[0]['Boys']:
			data_[0]['boys_percentage'] = round(data_[0]['Boys'] / data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['boys_percentage'] = 0
		if data_[0]['Girls']:
			data_[0]['girls_percentage'] = round(data_[0]['Girls'] / data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['girls_percentage'] = 0
		if data_[0]['Mixed']:
			data_[0]['mixed_percentage'] = round(data_[0]['Mixed'] / data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['mixed_percentage'] = 0
		if data_[0]['primary_school'] :
			data_[0]['primary_percentage'] = round(data_[0]['primary_school'] /data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['primary_percentage'] = 0
		if data_[0]['Elementary'] :
			data_[0]['elementary_percentage'] = round(data_[0]['Elementary'] /data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['elementary_percentage'] = 0
		if data_[0]['Middle'] :
			data_[0]['middle_percentage'] = round(data_[0]['Middle'] /data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['middle_percentage'] = 0
		if data_[0]['Secondary'] :
			data_[0]['secondary_percentage'] = round(data_[0]['Secondary'] /data_[0]['Total_Schools'] * 100,1)
		else:
			data_[0]['secondary_percentage'] = 0
			
		if data_[0]['higher_secondary'] :
			data_[0]['high_sec_percentage'] = round(data_[0]['higher_secondary'] /data_[0]['Total_Schools'] * 100, 1)
		else:
			data_[0]['high_sec_percentage'] = 0
		if data_[0]['Toilet'] :
			data_[0]['toilet_percentage'] = round(data_[0]['Toilet'] /data_[0]['Functional'] * 100, 1)
		else:
			data_[0]['toilet_percentage'] = 0
		if data_[0]['Campus'] :
			data_[0]['campus_percentage'] = round(data_[0]['Campus'] /data_[0]['Total_Schools'] * 100, 1)
		else:
			data_[0]['campus_percentage'] = 0
		if data_[0]['adopted_school'] :
			data_[0]['adopted_school_percentage'] = round(data_[0]['adopted_school'] /data_[0]['Total_Schools'] * 100, 1)
		else:
			data_[0]['adopted_school_percentage'] = 0
		if data_[0]['Branch'] :
			data_[0]['branch_percentage'] = round(data_[0]['Branch'] /data_[0]['Total_Schools'] * 100, 1)
		else:
			data_[0]['branch_percentage'] = 0
		if data_[0]['having_building'] :
			data_[0]['having_building_percentage'] = round(data_[0]['having_building'] /data_[0]['Functional'] * 100, 1)
		else:
			data_[0]['having_building_percentage'] = 0
		if data_[0]['Shelterless'] :
			data_[0]['Shelterless_percentage'] = round(data_[0]['Shelterless'] /data_[0]['Functional'] * 100, 1)
		else:
			data_[0]['Shelterless_percentage'] = 0
		if data_[0]['no_teacher'] :
			data_[0]['no_teacher_percentage'] = round(data_[0]['no_teacher'] /data_[0]['Closed'] * 100, 1)
		else:
			data_[0]['no_teacher_percentage'] = 0
		if data_[0]['no_enrollment'] :
			data_[0]['no_enrollment_percentage'] = round(data_[0]['no_enrollment'] /data_[0]['Closed'] * 100, 1)
		else:
			data_[0]['no_enrollment_percentage'] = 0
		if data_[0]['other_closure_reason'] :
			data_[0]['other_closure_reason_percentage'] = round(data_[0]['other_closure_reason'] /data_[0]['Closed'] * 100, 1)
		else:
			data_[0]['other_closure_reason_percentage'] = 0

	data_[0]['date_'] = frappe.utils.formatdate(data_[0]['date_'],"dd-MMM-yy")
	return data_

@frappe.whitelist()
def year_based_status(district=None, year=None):
    temp_query = """Select year,Sum(Case when status_detail="Functional" then 1 else 0 end) as functional, 
	SUM(CASE WHEN status_detail = "Closed" THEN 1 ELSE 0 END) as closed,
	SUM(no_of_merger_schools) as merged from tabASC where year <= "%s" and region = "%s"
	group by year limit 10""" % (year, district)
    data = frappe.db.sql(temp_query, as_dict=1)
    return data

def Merge(dict1, dict2):
    if len(dict1) == 0:
        return dict2
    else:
        return(dict2.update(dict1))

@frappe.whitelist()
def get_enrollment(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)
	temp_query= """SELECT case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END As "order", 
	SUM(enrol.boys) AS boys,
	SUM(enrol.girls) AS girls
	FROM `tabEnrolment Class and Gender wise` enrol  
	INNER JOIN tabASC on enrol.parent = tabASC.name
	WHERE tabASC.docstatus!=2 And tabASC.region = '%s' AND tabASC.year= '%s' 
	Group By case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END
    ORDER BY case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END asc"""%(district,year)
	data = frappe.db.sql(temp_query, as_dict=1)
	return {'enrols':data, 'year':year}

@frappe.whitelist()
def get_facility(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)


	temp_query = """Select
	SUM(
		CASE WHEN status_detail = "Functional" THEN 1 ELSE 0
	END
	) AS Functional,
	 SUM(
	IF(
		water_available = 'Yes'  ,
		1,
		0
	)
	)  AS drinking_water,
	SUM(
	IF(
		toilet_facility = 'Yes' ,
		1,
		0
	)
	) AS Toilet,
	SUM(
	IF(
		(electricity_connection = 'WAPDA/KE' OR electricity_connection = 'Solar System') ,
		1,
		0
	)
	) AS Electricity,
	SUM(
	IF(
		condition_of_boundary_wall = 'Satisfactory' OR condition_of_boundary_wall = 'Needs Repair' OR condition_of_boundary_wall = 'Dangerous',
		1,
		0
	)
	) AS boundary_wall,
		SUM(
	IF(
		play_ground_available = '1' ,
		1,
		0
	)
	) AS play_ground,
	SUM(
	IF(
		science_lab = 'Fully Functional' OR science_lab = 'Partially Functional' OR science_lab = 'Non Functional',
		1,
		0
	)
	) AS science_lab,
		SUM(
	IF(
		(library = 'Fully Functional' OR library = 'Partially Functional' OR library ='Non Functional') ,
		1,
		0
	)
	) AS library,
			SUM(
	IF(
		(computer_lab = 'Fully Functional' OR computer_lab = 'Partially Functional' OR computer_lab = 'Non Functional') ,
		1,
 	0
	)
	) AS computer_lab,
	SUM(
	IF(
		hand_wash_facility = 'Yes'  ,
		1,
		0
	)
	) AS hand_wash_facility,
		SUM(
		IF(
			l_availability_of_soap_at_hand_wash_ = 'Yes',
			1,
			0
		)
	) AS soap FROM tabASC where docstatus != 2 and status_detail = 'Functional' %s """%(condition)
	data = frappe.db.sql(temp_query, as_dict=1)

	temp_query= """SELECT 
    SUM(case When items = 'Electric Fans' or items = 'Solar Fans'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as fans,
    SUM(case When items = 'LED/TV for Student' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as tv,
    SUM(case When items = 'Multi Media / Projector' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as projector,
    SUM(case When items = 'Computers for Lab' or items = 'Computers'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as comp,
    
    SUM(case When (items = 'Electric Fans' or items = 'Solar Fans') and total > 0  Then 1 Else 0 END) as fans_exist,
    SUM(case When items = 'LED/TV for Student' and total > 0 Then 1 Else 0 END) as tv_exist,
    SUM(case When items = 'Multi Media / Projector' and total > 0 Then 1 Else 0 END) as projector_exist,
    SUM(case When (items = 'Computers for Lab' or items = 'Computers') and total > 0 Then 1 Else 0 END) as comp_exist


    FROM (Select name from tabASC tac where docstatus != 2 and status_detail= 'Functional' %s) tac_
    inner join  `tabStatus of Items availability` fac
    on tac_.name = fac.parent"""%(condition)
	data2 = frappe.db.sql(temp_query, as_dict=1)
	Merge(data2[0], data[0])


	if data[0]['drinking_water'] :
			data[0]['water_percentage'] = round(data[0]['drinking_water'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['water_percentage'] = 0
	if data[0]['Toilet'] :
		data[0]['toilet_percentage'] = round(data[0]['Toilet'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['toilet_percentage'] = 0
	if data[0]['Electricity'] :
		data[0]['electricity_percentage'] = round(data[0]['Electricity'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['electricity_percentage'] = 0
	if data[0]['boundary_wall'] :
		data[0]['boundary_wall_percentage'] = round(data[0]['boundary_wall'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['boundary_wall_percentage'] = 0
	if data[0]['science_lab'] :
		data[0]['science_lab_percentage'] = round(data[0]['science_lab'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['science_lab_percentage'] = 0
	if data[0]['library'] :
		data[0]['library_percentage'] = round(data[0]['library'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['library_percentage'] = 0
	if data[0]['computer_lab'] :
		data[0]['computer_lab_percentage'] = round(data[0]['computer_lab'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['computer_lab_percentage'] = 0			
	if data[0]['hand_wash_facility'] :
		data[0]['hand_wash_percentage'] = round(data[0]['hand_wash_facility'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['hand_wash_percentage'] = 0
	if data[0]['soap'] :
		data[0]['soap_percentage'] = round(data[0]['soap'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['soap_percentage'] = 0
	if data[0]['fans_exist'] :
		data[0]['fans_percentage'] = round(data[0]['fans_exist'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['fans_percentage'] = 0		
	if data[0]['tv_exist'] :
		data[0]['tv_percentage'] = round(data[0]['tv_exist'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['tv_percentage'] = 0		
	if data[0]['projector_exist'] :
		data[0]['proj_percentage'] = round(data[0]['projector_exist'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['proj_percentage'] = 0		
	if data[0]['comp_exist'] :
		data[0]['comp_percentage'] = round(data[0]['comp_exist'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['comp_percentage'] = 0		
	if data[0]['play_ground'] :
		data[0]['ground_percentage'] = round(data[0]['play_ground'] /data[0]['Functional'] * 100, 1)
	else:
		data[0]['ground_percentage'] = 0

	return data

@frappe.whitelist()
def get_staff(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)
	temp_query = """ Select 
	SUM(IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_non_government_male_staff,0)) as Non_Teaching_Male,
	SUM(IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) as Non_Teaching_Female
	from tabASC where docstatus != 2 %s
	"""%(condition)
	data = frappe.db.sql(temp_query,as_dict=1)

	staff_data_query = """SELECT designation_code AS designation, SUM(CASE when gender = 'Male' then 1 else 0 end) as male_staff,
	 SUM(CASE when gender = 'Female' then 1 else 0 end) as female_staff 
	 FROM
	(Select name from tabASC where tabASC.region = '%s' and tabASC.year= '%s' ) tac Inner JOIN
	`tabWorking Teaching Staff Detail` staff 
	on tac.name = staff.asc INNER JOIN tabDesignation des on des.name = staff.designation_code
	GROUP BY designation_code
	order by des.list_order"""% (district , str(year))
	staff_data = frappe.db.sql(staff_data_query,as_dict=1)
	if staff_data:
		for row in staff_data:
			if row['designation'] == 'Other':
				row['designation'] = 'Other Teaching Staff'

	data[0]['staff_data'] = staff_data
	return data


@frappe.whitelist()
def enrollment_ratio(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)
	temp_query = """ Select 
	SUM(sindhi_medium_enrolment) as sindhi,
	SUM(urdu_medium_enrolment) as urdu,
	SUM(english_medium_enrolment) as english,

	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(tac.total_teacher) ), 0) AS Students_Per_Teacher,
	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / COUNT(name) ), 0) AS Students_Per_School,
	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(total_rooms) ), 0) AS Students_Per_Classrooms,
	ROUND( ( SUM(tac.total_teacher) / COUNT(name) ), 0) AS Teachers_Per_School

	from tabASC tac where docstatus != 2 %s
	"""%(condition)
	data = frappe.db.sql(temp_query,as_dict=1)

	return data


@frappe.whitelist()
def taluka_data(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)


	temp_query = """ Select Count(name) as total_sch,
	SUM(CASE when status_detail = 'Functional' then 1 else 0 end ) functional,
	SUM(CASE when status_detail = 'Closed' then 1 else 0 end ) closed_,
	SUM(CASE when availability_of_building = 'Yes' and status_detail = 'Functional' then 1 else 0 end ) building,
	SUM(IFNULL(govt_male_teachers,0)+ IFNULL(non_govt_male_teachers,0)) male,
	SUM(IFNULL(govt_female_teachers,0)+ IFNULL(non_govt_female_teachers,0)) female,
	SUM(total_teacher) as total_teacher,
	
	SUM(male_enrollment) as boys,

	SUM(female_enrollment) as girls,
	SUM(total_enrollment) as total_enrol,

	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(tac.total_teacher) ), 0) AS Students_Per_Teacher,
	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / COUNT(name) ), 0) AS Students_Per_School,
	ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(total_rooms) ), 0) AS Students_Per_Classrooms,
	ROUND( ( SUM(tac.total_teacher) / COUNT(name) ), 0) AS Teachers_Per_School

	from tabASC tac where docstatus != 2 %s
	"""%(condition)
	data = frappe.db.sql(temp_query,as_dict=1)


	taluka_data_query = """Select district, 
		SUM(CASE when status_detail = 'Functional' then 1 else 0 end ) functional_schools,
		SUM(CASE when status_detail = 'Closed' then 1 else 0 end ) closed_schools,
		SUM(CASE when availability_of_building = 'Yes' and status_detail = 'Functional' then 1 else 0 end ) building_schools,
		SUM(IFNULL(govt_male_teachers,0)+ IFNULL(non_govt_male_teachers,0)) male_teachers,
		SUM(IFNULL(govt_female_teachers,0)+ IFNULL(non_govt_female_teachers,0)) female_teachers,
		SUM(male_enrollment) as boys_enrol,
		SUM(female_enrollment) as girls_enrol,
		FORMAT(ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(total_teacher) ), 0) ,0)AS Students_Per_Teacher,
		FORMAT(ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / COUNT(name) ), 0) ,0)AS Students_Per_School,
		FORMAT(ROUND( (SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) / SUM(total_rooms) ), 0) ,0)AS Students_Per_Classrooms,
		FORMAT(ROUND( ( SUM(total_teacher) / COUNT(name) ), 0) ,0)AS Teachers_Per_School
		from  tabASC where year = '%s' and region = '%s'
		GROUP BY district"""%(str(year), district)
	data_ = frappe.db.sql(taluka_data_query,as_dict=1)
	
	data[0]['taluka_data'] = data_
	return data

@frappe.whitelist()
def taluka_facility(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)
	# Facilities in Taluka
	facility_query_1 = """SELECT district,
	SUM(
	IF(
		water_available = 'Yes' ,
		1,
		0
	)
	)  AS drinking_water,
	SUM(
	IF(
		toilet_facility = 'No' OR toilet_facility = '' OR toilet_facility IS NULL,
		0,
		1
	)
	) AS Toilet,
	SUM(
	IF(
		electricity_connection = 'No Electricity Connection' OR electricity_connection = '' OR electricity_connection IS NULL,
		0,
		1
	)
	) AS Electricity,
	SUM(
	IF(
		condition_of_boundary_wall = 'No Boundary Wall' OR condition_of_boundary_wall = '' OR condition_of_boundary_wall IS NULL,
		0,
		1
	)
	) AS boundary_wall,
		SUM(
	IF(
		play_ground_available = '1',
		1,
		0
	)
	) AS play_ground,
	SUM(
	IF(
		science_lab = 'Not Available' OR science_lab = '' OR science_lab IS NULL,
		0,
		1
	)
	) AS science_lab,
		SUM(
	IF(
		library = 'Not Available' OR library = '' OR library IS NULL,
		0,
		1
	)
	) AS library,
			SUM(
	IF(
		computer_lab = 'Not Available' OR computer_lab = '' OR computer_lab IS NULL,
		0,
		1
	)
	) AS computer_lab,
	SUM(
	IF(
		hand_wash_facility = 'No' OR hand_wash_facility = '' OR hand_wash_facility IS NULL,
		0,
		1
	)
	) AS hand_wash_facility,
		SUM(
	IF(
		l_availability_of_soap_at_hand_wash_ = 'No' OR l_availability_of_soap_at_hand_wash_ = '' OR l_availability_of_soap_at_hand_wash_ IS NULL,
		0,
		1
	)
	) AS soap
    from tabASC tac
    where  	docstatus != 2 and status_detail = 'Functional' %s group by district order by taluka"""%(condition)

	facility_query_2="""SELECT district,

    SUM(case When items = 'Electric Fans' or items = 'Solar Fans'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as fans,
    SUM(case When items = 'LED/TV for Student' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as tv,
    SUM(case When items = 'Multi Media / Projector' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as projector,
    SUM(case When items = 'Computers for Lab' or items = 'Computers'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as comp
     



    FROM (Select name,district, year
          from tabASC tac where docstatus != 2 and status_detail= 'Functional' %s) t
    inner join  `tabStatus of Items availability` fac
    on t.name = fac.parent  group by district order by district """%(condition)

	data_1 =frappe.db.sql(facility_query_1,as_dict=1)
	data_2 =frappe.db.sql(facility_query_2,as_dict=1)


	for row in data_1:
		for r in data_2:
			if row['district'] == r['district']:
				row['fans'] = r['fans']
				row['comp'] = r['comp']
				row['projector'] = r['projector']
				row['tv'] = r['tv']


	return {"taluka_fac":data_1}

@frappe.whitelist()
def line_graph_data(district=None, year=None):
	condition = " and year= '%s' " % str(year)
	if district:
		condition += " and region= '%s' " % str(district)
	teacher_graph_query = """SELECT year,SUM(govt_male_teachers + non_govt_male_teachers+ govt_female_teachers + non_govt_female_teachers)
	as "teachers", SUM(total_enrollment) as enrollment FROM `tabASC` where year <= "%s" and region = "%s"
	group by year limit 10""" % (str(year), district)
	teacher_data = frappe.db.sql(teacher_graph_query, as_dict=1)
	date = frappe.utils.nowdate()
	date = frappe.utils.formatdate(date,"dd-MMM-yy")
	data = {
		'teacher_data' : teacher_data,
		'date': date
	}
	return data


