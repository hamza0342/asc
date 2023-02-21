import frappe
import requests
import json
@frappe.whitelist()
def get_data(school = None, year = None):
    condition = " and tac.year= '%s' " % str(year)
    if school :
        condition += " and tac.semis_code= '%s' " % str(school)

    temp_query = """SELECT
    tac.name,
    tac.semis_code,
    tac.region,
    IFNULL(FORMAT(tac.lat_n,6),"-")AS lat,
    IFNULL(FORMAT(tac.lon_e,6),"-")AS lon,
    IFNULL(ddo_cost_center,"-") as ddo,
    IFNULL(school_administration,"-") as admin,
    IFNULL(tac.district,"-")AS district,
    IFNULL(tac.taluka,"-")AS taluka,
    IFNULL(tac.uc,"-") AS union_council,
    IFNULL(tac.school_name,"-") AS school_name,
    tac.year AS year,
    IFNULL(tac.level, "-") AS level,
    IFNULL(tac.school_gender,"-") AS school_gender,
    IFNULL(tac.shift,"-") AS shift,
    IFNULL(tac.present_address,"-") AS address,
    IFNULL(tac.ena_constituency,"-") AS na,
    IFNULL((govt_male_teachers + non_govt_male_teachers),"-") AS male_teachers,
    IFNULL(govt_male_teachers,"-") AS ggggg,
    IFNULL(non_govt_male_teachers, "-") AS non_govt_male_teachers,
    IFNULL((total_teacher + total_non_teaching_staff),"-") AS total_staff,
	(IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_non_government_male_staff,0)) as Non_Teaching_Male,
	(IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) as Non_Teaching_Female,
    IFNULL(tac.status_detail,"-") AS status,
    IFNULL(tac.school_duration_of_closure,"-") AS duration,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(tac.location,"-") AS location,
    IFNULL (tac.school_phone_no,"-") AS phone,
    IFNULL(tac.fps_constituency,"-") AS pp,
    IFNULL( (govt_female_teachers + non_govt_female_teachers),"-") AS female_teachers,
    IFNULL(govt_female_teachers, 0) AS govt_female_teachers,
    IFNULL(non_govt_female_teachers, 0) AS non_govt_female_teachers,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments,
    IFNULL(tac.availability_of_building,"-") as have_building,
    IFNULL(tac.no_relevant_code,"-") as no_relevant_code,
    IFNULL(tac.no_relevant_other,"-") as no_relevant_other,
    IFNULL(tac.yes_relevant_code,"-") AS  ownership,
    IFNULL(tac.type_of_building,"-") AS construction_type,
    IFNULL(tac.condition_of_building, "-") AS condition_ ,
    IFNULL(tac.total_rooms_school,"-") AS total_rooms,
    IFNULL(tac.total_rooms, "-") AS classrooms,
    IFNULL(tac.total_area_school, "-") AS area,
    IFNULL(tac.is_campus_school, "-") AS is_campus_school,
    IFNULL(tac.hand_wash_facility, "-") AS hand_wash,
    IFNULL(tac.water_available,"-") AS drinking_water,
    IFNULL(tac.toilet_facility,"-") AS toilets,
    IFNULL(tac.total_no_of_functional_toilets,"0") AS no_toilets,
    IFNULL(tac.electricity_connection,"-") AS electricity,
    IF( tac.condition_of_boundary_wall IS NULL OR tac.condition_of_boundary_wall = "" OR tac.condition_of_boundary_wall = "No Boundary Wall" , "No", "Yes" ) AS boundary_wall,
    IFNULL(IF(tac.library = 'Not Available' or tac.library IS NULL ,"No","Yes"),"-") as "library",
    IFNULL(IF(science_lab = 'Not Available' or science_lab IS NULL ,"No","Yes"),"-") as "science_lab",
    IFNULL(IF(computer_lab = 'Not Available' or computer_lab IS NULL ,"No","Yes"),"-") as computer_lab,
    IFNULL(IF(play_ground_available=1,"Yes","No"),"-") "play_ground",
    IFNULL(play_ground_area_in_ft,"") as play_ground_area,
     
    IFNULL(no_of_sef_schools,"-") AS sef,
    IFNULL(l_availability_of_soap_at_hand_wash_,"-") AS soap,
    IFNULL(no_of_private_schools, "-") AS private_schools,
    IFNULL(total_surrounding_schools, "-") AS total_surr,
    
    IFNULL((CASE  
    WHEN urdu_medium_enrolment>0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment=0 THEN "Urdu"
    WHEN urdu_medium_enrolment=0 AND english_medium_enrolment>0 AND sindhi_medium_enrolment=0 THEN "English" 
    WHEN urdu_medium_enrolment=0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment>0 THEN "Sindhi"
    ELSE "Mixed"
    END),"-") AS school_medium,
    smc_received_detail as smc_received,
    IFNULL(t_r_smc,0) as amount_received,
    IFNULL(learning_teacher_material,0) as learning,
    IFNULL(m_repair,0) as maintainance,
    IFNULL(covid_essential_items,0) AS covid_essential_items,
    IFNULL(total_utilized,"0") AS total_utilized,
    IFNULL(principal_hm_name,"-") as hm_name,
    IFNULL(principal_designation,"-") as hm_designation,
    IFNULL(principal_phone,"-") as hm_phone,
    IFNULL(principal_gender,"-") as hm_gender,
    IFNULL(cnic_number_principal,"-") as hm_cnic,
    
    IFNULL(name_enumerator,"-") as deo_name,
    IFNULL(contact_no_enumerator,"-") as deo_phone,
    IFNULL(cnic_no_enumerator,"-") as deo_cnic,
    IFNULL(designation_enumerator,"-") as deo_designation,
    IFNULL(adopted_school,"-") as adopted_school,
    IFNULL(adopter_name,"-") as adopter_name,
    IFNULL(total_surrounding_schools , "-") as surrounding,
    IFNULL(sindhi_medium_enrolment) as sindhi_enrollment,
    IFNULL(english_medium_enrolment) as english_enrollment,
    IFNULL(urdu_medium_enrolment) as urdu_enrollment,


    CURDATE() AS date_
    


    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s Limit 1""" % (condition)

    data_ = frappe.db.sql(temp_query, as_dict=1) 
    if not data_:
        return 1

    asc = data_[0]['name']
    prefix_ = {"school_prefix": str(data_[0]['school_name']).split(" ")[0]}
    data_[0]['date_'] = frappe.utils.formatdate(data_[0]['date_'],"dd-MMM-yy")
    
    Merge(prefix_ , data_[0])
    #Code for basic facilities
    facility_query = """SELECT 
    SUM(case When items = 'Student Chairs / Single Desk' Then total Else 0 END) AS student_chairs, 
    SUM(case When items = 'Student Dual Desks' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS student_desks, 
    SUM(case When items = 'Student Benches' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS bench, 
    SUM(case When items = 'Teacher Tables' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS teacher_tables, 
    SUM(case When items = 'Teacher Chairs' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS teacher_chairs, 
    SUM(case When items = 'Blackboards' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS blackboard, 
    SUM(case When items = 'White boards' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS whiteboard, 
    SUM(case When items = 'Almirahs' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as almirah,
    SUM(case When items = 'Electric Fans' or items = 'Solar Fans'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as fans,
    SUM(case When items = 'LED/TV for Student' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as tv,
    SUM(case When items = 'Multi Media / Projector' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as projector,
    SUM(case When items = 'Computers for Lab' or items = 'Computers'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as comp


    FROM `tabStatus of Items availability` 
    WHERE parent = '%s' group by parent""" %(asc)
    facility_data= frappe.db.sql(facility_query,as_dict=1)
    if len(facility_data)>0:
        Merge(facility_data[0] , data_[0])
    else:
        facility_data = {'student_chairs':'-', 'student_desks':'-','bench':'-', 'teacher_tables':'-','teacher_chairs':'-','blackboard':'-','whiteboard':'-','almirah':'-'}
        Merge(facility_data , data_[0])

    staff_data={}
    staff_query="""SELECT designation_code AS designation, SUM(CASE when gender = 'Male' then 1 else 0 end) as male_staff,
	 SUM(CASE when gender = 'Female' then 1 else 0 end) as female_staff 
	 FROM
	(Select name from tabASC where tabASC.name = '%s' ) tac Inner JOIN
	`tabWorking Teaching Staff Detail` staff 
	on tac.name = staff.asc 
    INNER JOIN tabDesignation des on des.name = staff.designation_code
	GROUP BY designation_code
    order by des.list_order""" % (asc)

    staff_data['staf'] = frappe.db.sql(staff_query, as_dict=1)
    if len(staff_data['staf']) == 0:
        staff_data['staf'].append({'designation': "No Data" , 'male_staff' : 0 ,'female_staff' : 0 })
    # if data_[0]['level']=="Secondary":
    
    adp_data={}
    adp_query="""SELECT IFNULL(adp_no,"-") as adp_no, IFNULL(adp_description, "-") as adp_description, IFNULL(adp_package, "-") as adp_package, IFNULL(adp_progress, "-") as adp_progress, IFNULL(adp_data_source,"-") as adp_data_source
	 FROM `tabADP Scheme` where semis_id=%s """ % (data_[0]['semis_code'])

    adp_data['adp_data'] = frappe.db.sql(adp_query, as_dict=1)
    #if len(adp_data['adp_data']) == 0:
    #   adp_data['adp_data'].append({'adp_no': "No Data" , 'adp_description' : "-" ,'adp_package' : "-", 'adp_data_source' : "-" })
    
    sec_query=""" SELECT 
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.boys ELSE 0 END) AS x_arts_general_boys,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.boys ELSE 0 END) AS  x_computer_boys,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.boys ELSE 0 END) AS x_commerce_boys, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.boys ELSE 0 END) AS x_others_boys,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.boys ELSE 0 END) AS x_bio_boys,
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.girls ELSE 0 END) AS x_arts_general_girls,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.girls ELSE 0 END) AS  x_computer_girls,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.girls ELSE 0 END) AS x_commerce_girls, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.girls ELSE 0 END) AS x_others_girls,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.girls ELSE 0 END) AS x_bio_girls,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.boys ELSE 0 END) AS ix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.boys ELSE 0 END) AS  ix_computer_boys,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.boys ELSE 0 END) AS ix_commerce_boys, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.boys ELSE 0 END) AS ix_others_boys,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.boys ELSE 0 END) AS ix_bio_boys,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.girls ELSE 0 END) AS ix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.girls ELSE 0 END) AS  ix_computer_girls,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.girls ELSE 0 END) AS ix_commerce_girls, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.girls ELSE 0 END) AS ix_others_girls,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.girls ELSE 0 END) AS ix_bio_girls
    FROM `tabEnrolment Class and Gender wise` as e 
    WHERE e.parent='%s'
        """ %(asc)
    # if data_[0]['level']=="Higher Secondary":
    groups_query="""SELECT 
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.boys ELSE 0 END) AS x_arts_general_boys,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.boys ELSE 0 END) AS  x_computer_boys,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.boys ELSE 0 END) AS x_commerce_boys, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.boys ELSE 0 END) AS x_others_boys,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.boys ELSE 0 END) AS x_bio_boys,
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.girls ELSE 0 END) AS x_arts_general_girls,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.girls ELSE 0 END) AS  x_computer_girls,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.girls ELSE 0 END) AS x_commerce_girls, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.girls ELSE 0 END) AS x_others_girls,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.girls ELSE 0 END) AS x_bio_girls,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.boys ELSE 0 END) AS ix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.boys ELSE 0 END) AS  ix_computer_boys,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.boys ELSE 0 END) AS ix_commerce_boys, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.boys ELSE 0 END) AS ix_others_boys,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.boys ELSE 0 END) AS ix_bio_boys,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.girls ELSE 0 END) AS ix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.girls ELSE 0 END) AS  ix_computer_girls,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.girls ELSE 0 END) AS ix_commerce_girls, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.girls ELSE 0 END) AS ix_others_girls,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.girls ELSE 0 END) AS ix_bio_girls,
    SUM(CASE WHEN e.class="Class-XII Others" THEN e.girls ELSE 0 END) AS iix_others_girls,
    SUM(CASE WHEN e.class="Class-XII Commerce" THEN e.girls ELSE 0 END) AS iix_commerce_girls,
    SUM(CASE WHEN e.class="Class-XII Computer" THEN e.girls ELSE 0 END) AS iix_computer_girls,
    SUM(CASE WHEN e.class="Class-XII Arts-General" THEN e.girls ELSE 0 END) AS iix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-XII Pre-Medical" THEN e.girls ELSE 0 END) AS iix_pre_medical_girls,
    SUM(CASE WHEN e.class="Class-XII Pre-Enginering" THEN e.girls ELSE 0 END) AS iix_pre_enginering_girls,
    SUM(CASE WHEN e.class="Class-XII Commerce" THEN e.boys ELSE 0 END) AS iix_commerce_boys,
    SUM(CASE WHEN e.class="Class-XII Computer" THEN e.boys ELSE 0 END) AS iix_computer_boys,
    SUM(CASE WHEN e.class="Class-XII Arts-General" THEN e.boys ELSE 0 END) AS iix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-XII Pre-Medical" THEN e.boys ELSE 0 END) AS iix_pre_medical_boys,
    SUM(CASE WHEN e.class="Class-XII Pre-Enginering" THEN e.boys ELSE 0 END) AS iix_pre_enginering_boys,
    SUM(CASE WHEN e.class="Class-XI Others" THEN e.girls ELSE 0 END) AS ii_others_girls,
    SUM(CASE WHEN e.class="Class-XI Commerce" THEN e.girls ELSE 0 END) AS ii_commerce_girls,
    SUM(CASE WHEN e.class="Class-XI Computer" THEN e.girls ELSE 0 END) AS ii_computer_girls,
    SUM(CASE WHEN e.class="Class-XI Arts-General" THEN e.girls ELSE 0 END) AS ii_arts_general_girls,
    SUM(CASE WHEN e.class="Class-XI Pre-Medical" THEN e.girls ELSE 0 END) AS ii_pre_medical_girls,
    SUM(CASE WHEN e.class="Class-XI Pre-Enginering" THEN e.girls ELSE 0 END) AS ii_pre_enginering_girls,
    SUM(CASE WHEN e.class="Class-XI Commerce" THEN e.boys ELSE 0 END) AS ii_commerce_boys,
    SUM(CASE WHEN e.class="Class-XI Computer" THEN e.boys ELSE 0 END) AS ii_computer_boys,
    SUM(CASE WHEN e.class="Class-XI Arts-General" THEN e.boys ELSE 0 END) AS ii_arts_general_boys,
    SUM(CASE WHEN e.class="Class-XI Pre-Medical" THEN e.boys ELSE 0 END) AS ii_pre_medical_boys,
    SUM(CASE WHEN e.class="Class-XI Pre-Enginering" THEN e.boys ELSE 0 END) AS ii_pre_enginering_boys
    FROM `tabEnrolment Class and Gender wise` as e 
    WHERE e.parent='%s'
        """ %(asc)
    enrol_query = """SELECT tabProgram.profile_order As "order", 
    SUM(enrol.boys) AS boys, SUM(enrol.girls) AS girls, 
    SUM(enrol.total_class) AS "total" 
    FROM `tabEnrolment Class and Gender wise` enrol 
    CROSS join tabProgram on enrol.class = tabProgram.name 
    Where enrol.parent = '%s' 
    Group By tabProgram.profile_order 
    ORDER BY tabProgram.profile_order asc""" %(asc)
    enrollment_query = """SELECT tabProgram.profile_order As "order", 
	SUM(enrol.boys) AS boys,
	SUM(enrol.girls) AS girls,
    SUM(enrol.total_class) AS "total"
	FROM `tabEnrolment Class and Gender wise` enrol
	CROSS join tabProgram on enrol.class = tabProgram.name 
	LEFT JOIN tabASC tac on enrol.parent = tac.name
	WHERE tac.docstatus!=2  and tac.semis_code = '%s' and year = '%s' Group By tabProgram.profile_order
	ORDER BY tabProgram.profile_order asc""" % (school,str(year))
    enrollment_data={}
    # enrollment = frappe.db.sql(enrollment_query, as_dict=1)
    enrollment = frappe.db.sql(enrol_query, as_dict=1)
    level = data_[0]['level']
    enrollment_data['enrollment'] = set_data(enrollment , level,str(year))
    if data_[0]['level'] == 'Secondary' :
        sec_enrol= frappe.db.sql(sec_query, as_dict=1)
        for sec in sec_enrol[0].items():
            data_[0][sec[0]] = sec[1]

    if data_[0]['level'] == 'Higher Secondary' :
        sec_enrol= frappe.db.sql(sec_query, as_dict=1)
        for sec in sec_enrol[0].items():
            data_[0][sec[0]] = sec[1]
        enrol_group= frappe.db.sql(groups_query, as_dict=1)
        for en in enrol_group[0].items():
            data_[0][en[0]] = en[1]
    district = data_[0]['district']
    population = frappe.db.sql("Select total_population from `tabDistrict Population` where parent = '%s' and year = '%s' " %(district,str(year)))


    district_query = """SELECT   
    SUM(sindhi_medium_enrolment + urdu_medium_enrolment + english_medium_enrolment) AS district_enrolments,
    FORMAT(SUM(total_teacher),0) AS district_teachers,
    FORMAT(SUM(non_teaching_male_staff + non_teaching_female_staff),0) as district_non_teachers
    FROM tabASC Where docstatus!=2 and tabASC.district =  '%s' and year = '%s' """ %(district,str(year))

    district_data={}
    district_data['district_data'] = frappe.db.sql(district_query, as_dict=1)
    if population:
        district_data['district_data'][0]['ger'] = round((int(district_data['district_data'][0]['district_enrolments'])/int(population[0][0])) * 100 , 2)
    else:
        district_data['district_data'][0]['ger'] = '-'
    total_schools = frappe.db.sql("Select count(name) as district_schools from tabSchool where district = '%s' and enabled = 1" %(data_[0]['district']),as_dict=1)
    Merge(total_schools[0],district_data['district_data'][0]) 
    Merge(district_data , data_[0])

    near_by = """Select IFNULL(sur.semis_code, "No School") AS "near_semis", 
    IFNULL(school_name_prefix_and_name, "-") As "near_school", 
    IFNULL(type_of_school_see_codes, "-") as "near_type" FROM `tabSurrounding Government Schools` sur 
    RIGHT JOIN tabASC on sur.parent = tabASC.name 
    where tabASC.semis_code = '%s' and year = '%s' """ %(school,str(year))
    near_data_={}
    Merge(staff_data , data_[0])
    Merge(enrollment_data , data_[0])
    Merge(adp_data , data_[0])
    
################## get school_id from api
    idd = 123456
    get_school_id = requests.get("https://mne.seld.gos.pk/Services/api/Schools/GetSchoolBySEMISCode/" + data_[0]['semis_code'])
    get_school_id = json.loads(get_school_id.text)
    if get_school_id:
        idd = get_school_id["School_ID"]

################# fetch monitoring_id by using above school id
    get_monitoring_id = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetMonitoringBySchoolId", params = {'schoolId': str(idd)})
    get_monitoring_id = json.loads(get_monitoring_id.text)
    get_monitoring_status = get_monitoring_id['Status']
    monitoring_id = 0
    monitoring_date = None
    monitored_by = None
    if get_monitoring_status:
        get_dat = get_monitoring_id['Data']
        if len(get_dat) > 0 and get_dat[0].get('Monitoring_ID'):
            monitoring_id = get_dat[0]['Monitoring_ID']
            monitoring_date = get_dat[0]['Monitoring_Date']
            monitored_by = get_dat[0]['NAME']

    
################# fetch teacher data by using above monitoring_id
    get_teacher_data = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetTeachersAttendanceByMonitoringId", params = {'MonitoringId': str(monitoring_id)})
    get_teacher_data = json.loads(get_teacher_data.text)
    get_tch_status = get_teacher_data['Status']
    teacher_list = []
    if get_tch_status:
        teacher_list = get_teacher_data['Data']
    teachers_data = {'teachers_data': teacher_list}
    Merge(teachers_data , data_[0])
    
################# fetch student data by using above monitoring_id
    get_student_data = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetEnrolmentsByMonitoringId", params = {'MonitoringId': str(monitoring_id)})
    get_student_data = json.loads(get_student_data.text)
    get_stu_status = get_student_data['Status']
    students_list = []
    if get_stu_status:
        classes_list = ['Katchi', 'ClassI', 'ClassII', 'ClassIII', 'ClassIV', 'ClassV', 'ClassVI', 'ClassVII', 'ClassVIII', 'ClassIX_2', 'ClassIX_3_1', 'ClassIX_3_2', 'ClassIX_4', 'ClassIX_5', 'ClassX_6', 'ClassX_7_3', 'ClassX_7_4', 'ClassX_8', 'ClassX_9', 'ClassXI_10', 'ClassXI_11_5', 'ClassXI_11_6', 'ClassXI_11_7', 'ClassXI_12', 'ClassXI_13', 'ClassXII_14', 'ClassXII_15_8', 'ClassXII_15_9', 'ClassXII_15_10', 'ClassXII_16', 'ClassXII_17']
        for class_ in classes_list:
            male_enroll = female_enroll = male_p = female_p = 0
            if get_student_data['Data'][0]["KRAName"] == 'Total Male Students':
                male_enroll = int(get_student_data['Data'][0][str(class_)])
            if get_student_data['Data'][1]["KRAName"] == 'Total Female Students':
                female_enroll = int(get_student_data['Data'][1][str(class_)])
            if get_student_data['Data'][2]["KRAName"] == 'Total Male Students Present':
                male_p = int(get_student_data['Data'][2][str(class_)])
            if get_student_data['Data'][3]["KRAName"] == 'Total Female Students Present':
                female_p = int(get_student_data['Data'][3][str(class_)])
            if male_enroll > 0 or female_enroll > 0:
                dist_ = {'class': str(class_), 'male_enroll': male_enroll, 'female_enroll': female_enroll, 'total_enroll': int(male_enroll)+int(female_enroll), 'male_p': male_p, 'female_p': female_p, 'total_p': int(male_p)+int(female_p)}
                students_list.append(dist_)
    student_data= {'student_data': students_list}
    Merge(student_data , data_[0])
    return data_

def Merge(dict1, dict2):
    if len(dict1) == 0:
        return dict2
    else:
        return(dict2.update(dict1))

def set_data(data_ , level,year):
    data = data_
    if level == "Primary":
        max=6
        count = 1
        for row in data:
            if count == 7:
                break
            if row['order'] != count:
                loop = count
                for n in range(loop, row['order']):
                    data.append({'order': count, 'boys': 0, 'girls': 0, 'total': 0})
                    count +=1
            if count == len(data):
                for n in range(count, max):
                    data.append({'order': count +1, 'boys': 0, 'girls': 0, 'total': 0})
            count +=1
        if year == "2021-22":
            data = data[0:7]
        else:
            data = data[0:6]

    if level == "Middle" or level == "Elementary":
        max=9
        count = 1
        for row in data:
            if count == 10:
                break
            if row['order'] != count:
                loop = count
                for n in range(loop, row['order']):
                    data.append({'order': count, 'boys': 0, 'girls': 0, 'total': 0})
                    count +=1
            if count == len(data):
                for n in range(count, max):
                    data.append({'order': count +1, 'boys': 0, 'girls': 0, 'total': 0})
            count +=1
        if year == "2021-22":
            data = data[0:10]
        else:
            data = data[0:9]

    if level == "Secondary" :
        max=11
        count = 1
        for row in data:
            if count == 12:
                break
            if row['order'] != count:
                loop = count
                for n in range(loop, row['order']):
                    data.append({'order': count, 'boys': 0, 'girls': 0, 'total': 0})
                    count +=1
            if count == len(data):
                for n in range(count, max):
                    data.append({'order': count +1, 'boys': 0, 'girls': 0, 'total': 0})
            count +=1
        if year == "2021-22":
            data = data[0:12]
        else :
            data = data[0:11]

    if level == "Higher Secondary":
        max=13
        count = 1
        for row in data:
            if count == 14:
                break
            if row['order'] != count:
                loop = count
                for n in range(loop, row['order']):
                    data.append({'order': count, 'boys': 0, 'girls': 0, 'total': 0})
                    count +=1
            if count == len(data):
                for n in range(count, max):
                    data.append({'order': count +1, 'boys': 0, 'girls': 0, 'total': 0})
            count +=1
        if year == "2021-22":
            data = data[0:]
        else:
            data = data[0:]
    data = sorted(data, key = lambda i: i['order'])   
    return data



@frappe.whitelist()
def basic_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    year,
    name,
    semis_code,
    IFNULL(tac.availability_of_building,"-") as have_building,
    IFNULL(tac.district,"-")AS district,
    IFNULL(tac.taluka,"-")AS taluka,
    IFNULL(tac.uc,"-") AS union_council,
    IFNULL(tac.school_name,"-") AS school_name,
    IFNULL(tac.present_address,"-") AS address,
    IFNULL (tac.school_phone_no,"-") AS phone,
    IFNULL(tac.location,"-") AS location,
    IFNULL(tac.level, "-") AS level,
    IFNULL(tac.school_gender,"-") AS school_gender,
    IFNULL((CASE  
    WHEN urdu_medium_enrolment>0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment=0 THEN "Urdu"
    WHEN urdu_medium_enrolment=0 AND english_medium_enrolment>0 AND sindhi_medium_enrolment=0 THEN "English" 
    WHEN urdu_medium_enrolment=0 AND english_medium_enrolment=0 AND sindhi_medium_enrolment>0 THEN "Sindhi"
    ELSE "Mixed"
    END),"-") AS school_medium,
    IFNULL(sindhi_medium_enrolment) as sindhi_enrollment,
    IFNULL(english_medium_enrolment) as english_enrollment,
    IFNULL(urdu_medium_enrolment) as urdu_enrollment,
    IFNULL(tac.shift,"-") AS shift,
    IFNULL(tac.status_detail,"-") AS status,
    IFNULL(tac.school_duration_of_closure,"-") AS duration,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(ddo_cost_center,"-") as ddo,
    IFNULL(school_administration,"-") as admin,
    IFNULL(tac.is_campus_school, "-") AS is_campus_school,
    IFNULL(adopted_school,"-") as adopted_school,
    IFNULL(adopter_name,"-") as adopter_name,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments,
    IFNULL(total_surrounding_schools , "-") as surrounding,
    IFNULL(principal_hm_name,"-") as hm_name,
    IFNULL(principal_designation,"-") as hm_designation,
    IFNULL(principal_phone,"-") as hm_phone
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    date = frappe.utils.nowdate()
    date = frappe.utils.formatdate(date,"dd-MMM-yy")
    data[0]['date']= date
    return data


@frappe.whitelist()
def building_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(tac.availability_of_building,"-") as have_building,
    IFNULL(tac.no_relevant_code,"-") as no_relevant_code,
    IFNULL(tac.no_relevant_other,"-") as no_relevant_other,
    IFNULL(tac.yes_relevant_code,"-") AS  ownership,
    IFNULL(tac.type_of_building,"-") AS construction_type,
    IFNULL(tac.condition_of_building, "-") AS condition_ ,
    IFNULL(tac.total_rooms_school,"-") AS total_rooms,
    IFNULL(tac.total_rooms, "-") AS classrooms,
    IFNULL(tac.total_area_school, "-") AS area
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    return data

@frappe.whitelist()
def staff_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    name,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL((govt_male_teachers + non_govt_male_teachers),"-") AS male_teachers,
    IFNULL(govt_male_teachers,"-") AS ggggg,
    IFNULL(non_govt_male_teachers, "-") AS non_govt_male_teachers,
    IFNULL(non_govt_female_teachers, "-") AS non_govt_female_teachers,
    IFNULL(govt_female_teachers, 0) AS govt_female_teachers,
    IFNULL(tac.availability_of_building,"-") as have_building,
    

    IFNULL((total_teacher + total_non_teaching_staff),"-") AS total_staff,
	(IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_non_government_male_staff,0)) as Non_Teaching_Male,
	(IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) as Non_Teaching_Female,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments

    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    asc = data[0]['name']


    staff_data={}
    staff_query="""SELECT designation_code AS designation, SUM(CASE when gender = 'Male' then 1 else 0 end) as male_staff,
	 SUM(CASE when gender = 'Female' then 1 else 0 end) as female_staff 
	 FROM
	(Select name from tabASC where tabASC.name = '%s' ) tac Inner JOIN
	`tabWorking Teaching Staff Detail` staff 
	on tac.name = staff.asc 
    INNER JOIN tabDesignation des on des.name = staff.designation_code
	GROUP BY designation_code
    order by des.list_order""" % (asc)

    staff_data = frappe.db.sql(staff_query, as_dict=1)
    if len(staff_data) == 0:
        staff_data.append({'designation': "No Data" , 'male_staff' : 0 ,'female_staff' : 0 })
    data[0]['staf'] = staff_data

    return data


@frappe.whitelist()
def facility_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(tac.hand_wash_facility, "-") AS hand_wash,
    IFNULL(tac.water_available,"-") AS drinking_water,
    IFNULL(tac.toilet_facility,"-") AS toilets,
    IFNULL(tac.total_no_of_functional_toilets,"0") AS no_toilets,
    IFNULL(tac.electricity_connection,"-") AS electricity,
    IF( tac.condition_of_boundary_wall IS NULL OR tac.condition_of_boundary_wall = "" OR tac.condition_of_boundary_wall = "No Boundary Wall" , "No", "Yes" ) AS boundary_wall,
    IFNULL(IF(tac.library = 'Not Available' or tac.library IS NULL ,"No","Yes"),"-") as "library",
    IFNULL(IF(science_lab = 'Not Available' or science_lab IS NULL ,"No","Yes"),"-") as "science_lab",
    IFNULL(IF(computer_lab = 'Not Available' or computer_lab IS NULL ,"No","Yes"),"-") as computer_lab,
    IFNULL(l_availability_of_soap_at_hand_wash_,"-") AS soap,
    IFNULL(IF(play_ground_available=1,"Yes","No"),"-") "play_ground",
    IFNULL(play_ground_area_in_ft,"") as play_ground_area
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1) 
    return data


@frappe.whitelist()
def item_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    name,
    IFNULL(tac.major_reason_closure,"-") AS reason

    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query)
    asc = data[0][0]
    frappe.msgprint(frappe.as_json(data))

    facility_query = """SELECT 
    SUM(case When items = 'Student Chairs / Single Desk' Then total Else 0 END) AS student_chairs, 
    SUM(case When items = 'Student Dual Desks' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS student_desks, 
    SUM(case When items = 'Student Benches' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS bench, 
    SUM(case When items = 'Teacher Tables' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS teacher_tables, 
    SUM(case When items = 'Teacher Chairs' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS teacher_chairs, 
    SUM(case When items = 'Blackboards' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS blackboard, 
    SUM(case When items = 'White boards' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) AS whiteboard, 
    SUM(case When items = 'Almirahs' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as almirah,
    SUM(case When items = 'Electric Fans' or items = 'Solar Fans'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as fans,
    SUM(case When items = 'LED/TV for Student' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as tv,
    SUM(case When items = 'Multi Media / Projector' Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as projector,
    SUM(case When items = 'Computers for Lab' or items = 'Computers'  Then (IFNULL(working,0) + IFNULL(repairable,0)) Else 0 END) as comp


    FROM `tabStatus of Items availability` 
    WHERE parent = '%s' group by parent""" %(asc)
    facility_data= frappe.db.sql(facility_query,as_dict=1)
    if facility_data:
        facility_data[0]['reason'] = data[0][1]
    else:
        return 1

    return facility_data

@frappe.whitelist()
def enrollment_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select name,year,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments,
    level
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    asc = data[0]['name']
    level = data[0]['level']
    year = data[0]['year']

    enrol_query = """SELECT case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END As "order", 
	SUM(enrol.boys) AS boys,
	SUM(enrol.girls) AS girls,
	SUM(enrol.total_class) AS total

	FROM `tabEnrolment Class and Gender wise` enrol   
	WHERE enrol.parent = '%s'
	Group By case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END
    ORDER BY case when enrol.class='ECE' then 0 when enrol.class='Katchi' then 1 when enrol.class='Class-I' then 2 when enrol.class='Class-II' then 3 when enrol.class='Class-III' then 4 when enrol.class='Class-IV' then 5 when enrol.class='Class-V' then 6 when enrol.class='Class-VI' then 7 when enrol.class='Class-VII' then 8 when enrol.class='Class-VIII' then 9 when enrol.class='Class-IX Arts-General' then 10 when enrol.class='Class-IX Computer Arts-General' then 10 when enrol.class='Class-IX Biology' then 10 when enrol.class='Class-IX Commerce' then 10 when enrol.class='Class-IX Others' then 10 when enrol.class='Class-X Arts-General' then 11 when enrol.class='Class-X Computer' then 11 when enrol.class='Class-X Biology' then 11 when enrol.class='Class-X Commerce' then 11 when enrol.class='Class-X Others' then 11 when enrol.class='Class-XI Arts-General' then 12 when enrol.class='Class-XI Computer' then 12 when enrol.class='Class-XI Pre-Medical' then 12 when enrol.class='Class-XI Pre-Enginering' then 12 when enrol.class='Class-XI Commerce' then 12 when enrol.class='Class-XI Others' then 12 ELSE 13 END asc """%(asc)
    enrol_data = frappe.db.sql(enrol_query, as_dict=1)

    data[0]['enrollment'] = set_data(enrol_data , level,str(year))
    return data

@frappe.whitelist()
def secondary_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select name,year,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments,
    level
  
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    asc = data[0]['name']

    sec_query=""" SELECT 
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.boys ELSE 0 END) AS x_arts_general_boys,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.boys ELSE 0 END) AS  x_computer_boys,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.boys ELSE 0 END) AS x_commerce_boys, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.boys ELSE 0 END) AS x_others_boys,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.boys ELSE 0 END) AS x_bio_boys,
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.girls ELSE 0 END) AS x_arts_general_girls,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.girls ELSE 0 END) AS  x_computer_girls,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.girls ELSE 0 END) AS x_commerce_girls, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.girls ELSE 0 END) AS x_others_girls,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.girls ELSE 0 END) AS x_bio_girls,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.boys ELSE 0 END) AS ix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.boys ELSE 0 END) AS  ix_computer_boys,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.boys ELSE 0 END) AS ix_commerce_boys, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.boys ELSE 0 END) AS ix_others_boys,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.boys ELSE 0 END) AS ix_bio_boys,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.girls ELSE 0 END) AS ix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.girls ELSE 0 END) AS  ix_computer_girls,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.girls ELSE 0 END) AS ix_commerce_girls, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.girls ELSE 0 END) AS ix_others_girls,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.girls ELSE 0 END) AS ix_bio_girls
    FROM `tabEnrolment Class and Gender wise` as e 
    WHERE e.parent='%s'
        """ %(asc)
    sec_enrol= frappe.db.sql(sec_query, as_dict=1)
    for sec in sec_enrol[0].items():
            data[0][sec[0]] = sec[1]
    
    return data

@frappe.whitelist()
def hi_secondary_data(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select name,year,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    IFNULL(FORMAT((tac.urdu_medium_enrolment + tac.english_medium_enrolment + tac.sindhi_medium_enrolment), 0),0) AS enrollments,
    level
  
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    asc = data[0]['name']

    groups_query="""SELECT 
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.boys ELSE 0 END) AS x_arts_general_boys,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.boys ELSE 0 END) AS  x_computer_boys,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.boys ELSE 0 END) AS x_commerce_boys, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.boys ELSE 0 END) AS x_others_boys,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.boys ELSE 0 END) AS x_bio_boys,
    SUM(CASE WHEN e.class="Class-X Arts-General" THEN e.girls ELSE 0 END) AS x_arts_general_girls,
    SUM(CASE WHEN e.class="Class-X Computer" THEN e.girls ELSE 0 END) AS  x_computer_girls,
    SUM(CASE WHEN e.class="Class-X Commerce" THEN e.girls ELSE 0 END) AS x_commerce_girls, 
    SUM(CASE WHEN e.class="Class-X Others" THEN e.girls ELSE 0 END) AS x_others_girls,
    SUM(CASE WHEN e.class="Class-X Biology" THEN e.girls ELSE 0 END) AS x_bio_girls,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.boys ELSE 0 END) AS ix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.boys ELSE 0 END) AS  ix_computer_boys,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.boys ELSE 0 END) AS ix_commerce_boys, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.boys ELSE 0 END) AS ix_others_boys,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.boys ELSE 0 END) AS ix_bio_boys,
    SUM(CASE WHEN e.class="Class-IX Arts-General" THEN e.girls ELSE 0 END) AS ix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-IX Computer" THEN e.girls ELSE 0 END) AS  ix_computer_girls,
    SUM(CASE WHEN e.class="Class-IX Commerce" THEN e.girls ELSE 0 END) AS ix_commerce_girls, 
    SUM(CASE WHEN e.class="Class-IX Others" THEN e.girls ELSE 0 END) AS ix_others_girls,
    SUM(CASE WHEN e.class="Class-IX Biology" THEN e.girls ELSE 0 END) AS ix_bio_girls,
    SUM(CASE WHEN e.class="Class-XII Others" THEN e.girls ELSE 0 END) AS iix_others_girls,
    SUM(CASE WHEN e.class="Class-XII Commerce" THEN e.girls ELSE 0 END) AS iix_commerce_girls,
    SUM(CASE WHEN e.class="Class-XII Computer" THEN e.girls ELSE 0 END) AS iix_computer_girls,
    SUM(CASE WHEN e.class="Class-XII Arts-General" THEN e.girls ELSE 0 END) AS iix_arts_general_girls,
    SUM(CASE WHEN e.class="Class-XII Pre-Medical" THEN e.girls ELSE 0 END) AS iix_pre_medical_girls,
    SUM(CASE WHEN e.class="Class-XII Pre-Enginering" THEN e.girls ELSE 0 END) AS iix_pre_enginering_girls,
    SUM(CASE WHEN e.class="Class-XII Commerce" THEN e.boys ELSE 0 END) AS iix_commerce_boys,
    SUM(CASE WHEN e.class="Class-XII Computer" THEN e.boys ELSE 0 END) AS iix_computer_boys,
    SUM(CASE WHEN e.class="Class-XII Arts-General" THEN e.boys ELSE 0 END) AS iix_arts_general_boys,
    SUM(CASE WHEN e.class="Class-XII Pre-Medical" THEN e.boys ELSE 0 END) AS iix_pre_medical_boys,
    SUM(CASE WHEN e.class="Class-XII Pre-Enginering" THEN e.boys ELSE 0 END) AS iix_pre_enginering_boys,
    SUM(CASE WHEN e.class="Class-XI Others" THEN e.girls ELSE 0 END) AS ii_others_girls,
    SUM(CASE WHEN e.class="Class-XI Commerce" THEN e.girls ELSE 0 END) AS ii_commerce_girls,
    SUM(CASE WHEN e.class="Class-XI Computer" THEN e.girls ELSE 0 END) AS ii_computer_girls,
    SUM(CASE WHEN e.class="Class-XI Arts-General" THEN e.girls ELSE 0 END) AS ii_arts_general_girls,
    SUM(CASE WHEN e.class="Class-XI Pre-Medical" THEN e.girls ELSE 0 END) AS ii_pre_medical_girls,
    SUM(CASE WHEN e.class="Class-XI Pre-Enginering" THEN e.girls ELSE 0 END) AS ii_pre_enginering_girls,
    SUM(CASE WHEN e.class="Class-XI Commerce" THEN e.boys ELSE 0 END) AS ii_commerce_boys,
    SUM(CASE WHEN e.class="Class-XI Computer" THEN e.boys ELSE 0 END) AS ii_computer_boys,
    SUM(CASE WHEN e.class="Class-XI Arts-General" THEN e.boys ELSE 0 END) AS ii_arts_general_boys,
    SUM(CASE WHEN e.class="Class-XI Pre-Medical" THEN e.boys ELSE 0 END) AS ii_pre_medical_boys,
    SUM(CASE WHEN e.class="Class-XI Pre-Enginering" THEN e.boys ELSE 0 END) AS ii_pre_enginering_boys
    FROM `tabEnrolment Class and Gender wise` as e 
    WHERE e.parent='%s'
        """ %(asc)
    enrol_group= frappe.db.sql(groups_query, as_dict=1)
    for en in enrol_group[0].items():
        data[0][en[0]] = en[1]
    
    return data

@frappe.whitelist()
def smc_section(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    if school :
        condition += " and semis_code= '%s' " % str(school)
    temp_query = """Select
    name,year,
    semis_code,
    IFNULL(tac.major_reason_closure,"-") AS reason,
    smc_received_detail as smc_received,
    IFNULL(t_r_smc,0) as amount_received,
    IFNULL(Round(total_utilized,2),"0") AS total_utilized,
    IFNULL(principal_hm_name,"-") as hm_name,
    IFNULL(principal_designation,"-") as hm_designation,
    IFNULL(principal_phone,"-") as hm_phone
    FROM
    tabASC tac
    WHERE  tac.docstatus!=2 %s """ % (condition)
    data = frappe.db.sql(temp_query,as_dict=1)
    adp_data={}
    adp_query="""SELECT IFNULL(adp_no,"-") as adp_no, IFNULL(adp_description, "-") as adp_description, IFNULL(adp_package, "-") as adp_package, IFNULL(adp_progress, "-") as adp_progress, IFNULL(adp_data_source,"-") as adp_data_source
        FROM `tabADP Scheme` where semis_id=%s """ % (data[0]['semis_code'])

    adp_data['adp_data'] = frappe.db.sql(adp_query, as_dict=1)
    Merge(adp_data , data[0])
    date = frappe.utils.nowdate()
    date = frappe.utils.formatdate(date,"dd-MMM-yy")
    data[0]['date']= date

    return data



@frappe.whitelist()
def visit_section(school = None, year = None):
    condition = " and year= '%s' " % str(year)
    data_ = None
    try:
        if school :
            condition += " and semis_code= '%s' " % str(school)
        
        temp_query = """Select
        name,year,
        semis_code

        FROM
        tabASC tac
        WHERE  tac.docstatus!=2 %s """ % (condition)
        data_ = frappe.db.sql(temp_query,as_dict=1)
        ################## get school_id from api
        idd = 123456
        get_school_id = requests.get("https://mne.seld.gos.pk/Services/api/Schools/GetSchoolBySEMISCode/" + data_[0]['semis_code'])
        get_school_id = json.loads(get_school_id.text)
        if get_school_id:
            idd = get_school_id["School_ID"]

    ################# fetch monitoring_id by using above school id
        get_monitoring_id = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetMonitoringBySchoolId", params = {'schoolId': str(idd)})
        get_monitoring_id = json.loads(get_monitoring_id.text)
        get_monitoring_status = get_monitoring_id['Status']
        monitoring_id = 0
        monitoring_date = None
        monitored_by = None

        if get_monitoring_status:
            get_dat = get_monitoring_id['Data']
            if len(get_dat) > 0 and get_dat[0].get('Monitoring_ID'):
                monitoring_id = get_dat[0]['Monitoring_ID']
                monitoring_date = get_dat[0]['Monitoring_Date']
                monitored_by = get_dat[0]['NAME']

        
    ################# fetch teacher data by using above monitoring_id
        get_teacher_data = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetTeachersAttendanceByMonitoringId", params = {'MonitoringId': str(monitoring_id)})
        get_teacher_data = json.loads(get_teacher_data.text)
        get_tch_status = get_teacher_data['Status']
        teacher_list = []
        if get_tch_status:
            teacher_list = get_teacher_data['Data']
        teachers_data = {'teachers_data': teacher_list}
        Merge(teachers_data , data_[0])
        
    ################# fetch student data by using above monitoring_id
        get_student_data = requests.get("https://mne.seld.gos.pk/Services/api//Schools/GetEnrolmentsByMonitoringId", params = {'MonitoringId': str(monitoring_id)})
        get_student_data = json.loads(get_student_data.text)
        get_stu_status = get_student_data['Status']
        students_list = []
        if get_stu_status:
            classes_list = ['Katchi', 'ClassI', 'ClassII', 'ClassIII', 'ClassIV', 'ClassV', 'ClassVI', 'ClassVII', 'ClassVIII', 'ClassIX_2', 'ClassIX_3_1', 'ClassIX_3_2', 'ClassIX_4', 'ClassIX_5', 'ClassX_6', 'ClassX_7_3', 'ClassX_7_4', 'ClassX_8', 'ClassX_9', 'ClassXI_10', 'ClassXI_11_5', 'ClassXI_11_6', 'ClassXI_11_7', 'ClassXI_12', 'ClassXI_13', 'ClassXII_14', 'ClassXII_15_8', 'ClassXII_15_9', 'ClassXII_15_10', 'ClassXII_16', 'ClassXII_17']
            for class_ in classes_list:
                male_enroll = female_enroll = male_p = female_p = 0
                if get_student_data['Data'][0]["KRAName"] == 'Total Male Students':
                    male_enroll = int(get_student_data['Data'][0][str(class_)])
                if get_student_data['Data'][1]["KRAName"] == 'Total Female Students':
                    female_enroll = int(get_student_data['Data'][1][str(class_)])
                if get_student_data['Data'][2]["KRAName"] == 'Total Male Students Present':
                    male_p = int(get_student_data['Data'][2][str(class_)])
                if get_student_data['Data'][3]["KRAName"] == 'Total Female Students Present':
                    female_p = int(get_student_data['Data'][3][str(class_)])
                if male_enroll > 0 or female_enroll > 0:
                    dist_ = {'class': str(class_), 'male_enroll': male_enroll, 'female_enroll': female_enroll, 'total_enroll': int(male_enroll)+int(female_enroll), 'male_p': male_p, 'female_p': female_p, 'total_p': int(male_p)+int(female_p)}
                    students_list.append(dist_)
        student_data= {'student_data': students_list}
        Merge(student_data , data_[0])
        date = frappe.utils.nowdate()
        date = frappe.utils.formatdate(date,"dd-MMM-yy")
        data_[0]['date_']= date

        date_ = monitoring_date.split("T")[0]
        date_ = frappe.utils.formatdate(date_,"dd-MMM-yy")

        data_[0]['date']= date_
        data_[0]['monitored_by']= monitored_by
    except:
        data_[0]['name']="Data not found due to network problem"

    return data_