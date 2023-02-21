# Copyright (c) 2021, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import utils
from frappe.model.document import Document


class ASC(Document):
    def validate(self):
        # self.check_negative_values()
        # self.validation_for_semis_code()
        self.check_child_tables()
        self.check_school_medium()
        self.add_items()
    def on_update(self):
        self.set_school_criteria()
        self.update_kpi()
    
    def after_delete(self):
        kpi_exist = frappe.get_doc("ASC_KPI",self.name)
        if kpi_exist:
            kpi_exist.delete()


    def add_items(self):
        if not self.ecce:
            self.ecce = 0
        if not self.post_primary:
            self.post_primary = 0
        if not self.primary:
            self.primary = 0  
        self.total_rooms = self.ecce + self.post_primary + self.primary

        if not self.minority_boys:
            self.minority_boys = 0
        if not self.minority_girls:
            self.minority_girls = 0
        self.minority_total = self.minority_boys + self.minority_girls

        if not self.govt_male_teachers:
            self.govt_male_teachers=0
        if not self.govt_female_teachers:
            self.govt_female_teachers =0
        if not self.non_govt_male_teachers:
            self.non_govt_male_teachers=0
        if not self.non_govt_female_teachers:
            self.non_govt_female_teachers=0
        self.total_teacher = self.govt_male_teachers + self.govt_female_teachers + self.non_govt_male_teachers + self.non_govt_female_teachers

        if not self.non_teaching_male_staff:
            self.non_teaching_male_staff=0
        if not self.non_teaching_female_staff:
            self.non_teaching_female_staff=0
        self.total_non_teaching_staff = self.non_teaching_male_staff + self.non_teaching_female_staff

        if not self.non_teaching_non_government_male_staff:
            self.non_teaching_non_government_male_staff = 0
        if not self.non_teaching_non_government_female_staff:
            self.non_teaching_non_government_female_staff = 0
        self.total_non_teaching_non_government_staff= self.non_teaching_non_government_male_staff + self.non_teaching_non_government_female_staff

        if not self.covid_essential_items:
            self.covid_essential_items=0
        if not self.m_repair:
            self.m_repair=0
        if not self.learning_teacher_material:
            self.learning_teacher_material=0
        self.total_utilized = float(self.learning_teacher_material) + float(self.m_repair) + float(self.covid_essential_items)

        if not self.polio_affected:
            self.polio_affected =0
        if not self.physical_disabilites:
            self.physical_disabilites = 0
        self.total_disable_students = int(self.polio_affected) + int(self.physical_disabilites)


        if not self.no_of_sef_schools:
            self.no_of_sef_schools = 0
        if not self.no_of_private_schools:
            self.no_of_private_schools=0
        self.total_surrounding_schools = int(self.no_of_private_schools) + int(self.no_of_sef_schools)
    

    def check_school_medium(self):
        if not self.sindhi_medium_enrolment:
            self.sindhi_medium_enrolment = 0
        if not self.urdu_medium_enrolment:
            self.urdu_medium_enrolment = 0
        if not self.english_medium_enrolment:
            self.english_medium_enrolment = 0
        sindhi, urdu, english = int(self.sindhi_medium_enrolment), int(
            self.urdu_medium_enrolment), int(self.english_medium_enrolment)
        self.school_type = ""

        if sindhi > 0 and urdu == 0 and english == 0:
            self.school_type = 'Sindhi'
        if sindhi == 0 and urdu > 0 and english == 0:
            self.school_type = 'Urdu'
        if sindhi == 0 and urdu == 0 and english > 0:
            self.school_type = 'English'
        if ((sindhi > 0 and urdu > 0) or (sindhi > 0 and english > 0) or (urdu > 0 and english > 0)):
            self.school_type = 'Mixed'

    def check_child_tables(self):
        if len(self.gender_wise_enrolment) >= 1:
            final_tt = 0
            self.female_enrollment = 0
            self.male_enrollment = 0
            for xx in self.gender_wise_enrolment:
                if self.school_gender == 'Girls':
                    if not xx.girls:
                        xx.girls = 0
                        pass
                    if not xx.boys:
                        xx.boys = 0
                    xx.total = xx.girls + xx.boys
                    self.female_enrollment = self.female_enrollment + xx.girls
                    final_tt += xx.total_class

                if self.school_gender == 'Boys':
                    if not xx.boys:
                        xx.boys = 0
                    if not xx.girls:
                        xx.girls = 0
                    xx.total = xx.boys  + xx.girls
                    final_tt += xx.total_class
                    self.male_enrollment = self.male_enrollment + xx.boys

                if self.school_gender == 'Mixed':
                    if not xx.boys:
                        xx.boys = 0
                    if not xx.girls:
                        xx.girls = 0
                        pass
                    xx.total_class = xx.boys + xx.girls
                    final_tt += xx.total_class
                    self.male_enrollment = self.male_enrollment + xx.boys
                    self.female_enrollment = self.female_enrollment + xx.girls

                #xx.overall_total = final_tt
                self.total_enrollment = final_tt

        if len(self.table_repeaters) >= 1:
            final_tt = 0
            self.male_repeaters = 0
            self.female_repeaters = 0
            for xx in self.table_repeaters:
                if self.school_gender == 'Girls':
                    if not xx.girls:
                        xx.girls = 0
                        pass
                    if not xx.boys:
                        xx.boys = 0
                    xx.total = xx.girls + xx.boys
                    self.female_repeaters = self.female_repeaters + xx.girls
                    final_tt += xx.total

                if self.school_gender == 'Boys':
                    if not xx.boys:
                        xx.boys = 0
                    if not xx.girls:
                        xx.girls = 0
                    xx.total = xx.boys  + xx.girls
                    self.male_repeaters = self.male_repeaters + xx.boys
                    final_tt += xx.total

                if self.school_gender == 'Mixed':
                    if not xx.boys:
                        xx.boys = 0
                    if not xx.girls:
                        xx.girls = 0
                        pass
                    xx.total = xx.boys + xx.girls
                    final_tt += xx.total
                    self.male_repeaters = self.male_repeaters + xx.boys
                    self.female_repeaters = self.female_repeaters + xx.girls
                #xx.overall = final_tt
                self.total_repeaters = final_tt
        if not self.polio_affected:
            self.polio_affected = 0
        if not self.physical_disabilites:
            self.physical_disabilites = 0
        self.total_disables = self.polio_affected + self.physical_disabilites

    def validation_for_semis_code(self):
        if self.share_building_code:
            response = share_semis_code(
                self.share_building_code, self.district, self.semis_code)
            if response[0] == 1:
                self.share_building_code = ''
                self.shared_school_name = ''
                frappe.throw("District should be same for both schools")
            else:
                self.shared_school_name = response[1]

        if self.adjacent_schools:
            for x in self.adjacent_schools:
                if x.semis_code:
                    response = share_semis_code(
                        x.semis_code, self.district, self.semis_code)
                    if response[0] == 1:
                        self.semis_code = ''
                        frappe.throw(
                            "District should be same for both schools")
                    else:
                        self.school_name_prefix_and_name = response[1]

        if self.semis:
            response = share_semis_code(
                self.semis, self.district, self.semis_code)
            if response[0] == 1:
                self.semis = ''
                frappe.throw("District should be same for both schools")
            else:
                self.name_of_main_school = response[1]

    def check_negative_values(self):
        # if self.share_building_code and self.share_building_code < 0:
        # 	frappe.throw("Number is negative at section 3 (c)")

        if self.rooms_used_as_class and self.rooms_used_as_class < 0:
            frappe.throw("Number is negative at section 3 (g)")

        if self.total_rooms and self.total_rooms < 0:
            frappe.throw("Number is negative at section 3 (h)")

        if self.ecce and self.ecce < 0:
            frappe.throw("Number is negative at Section 3 (ecce)")

        if self.primary and self.primary < 0:
            frappe.throw("Number is negative at Section 3 (primary)")

        if self.post_primary and self.post_primary < 0:
            frappe.throw("Number is negative at Section 3 (post_primary)")

        if self.total_no_of_functional_toilets and self.total_no_of_functional_toilets < 0:
            frappe.throw(
                "Number is negative at Section 4 (total_no_of_functional_toilets)")

        if self.total_no_of_non_functional_toilet and self.total_no_of_non_functional_toilet < 0:
            frappe.throw(
                "Number is negative at Section 4 (total_no_of_non_functional_toilet)")

        if self.polio_affected and self.polio_affected < 0:
            frappe.throw("Number is negative at Section 4 (polio_affected)")

        if self.physical_disabilites and self.physical_disabilites < 0:
            frappe.throw(
                "Number is negative at Section 4 (physical_disabilites)")

        if self.semis and self.semis < 0:
            frappe.throw("Number is negative at Section 5 (b)")

        if self.no_of_merger_schools and self.no_of_merger_schools < 0:
            frappe.throw(
                "Number is negative at Section 5 (no_of_merger_schools)")

        if self.no_of_sef_schools and self.no_of_sef_schools < 0:
            frappe.throw("Number is negative at Section 5 (no_of_sef_schools)")

        if self.no_of_private_schools and self.no_of_private_schools < 0:
            frappe.throw(
                "Number is negative at Section 5 (no_of_private_schools)")

        if self.govt_male_teachers and self.govt_male_teachers < 0:
            frappe.throw(
                "Number is negative at Section 10 (govt_male_teachers)")

        if self.govt_female_teachers and self.govt_female_teachers < 0:
            frappe.throw(
                "Number is negative at Section 10 (govt_female_teachers)")

        if self.non_govt_male_teachers and self.non_govt_male_teachers < 0:
            frappe.throw(
                "Number is negative at Section 10 (non_govt_male_teachers)")

        if self.non_teaching_male_staff and self.non_teaching_male_staff < 0:
            frappe.throw(
                "Number is negative at Section 10 (non_teaching_male_staff)")

        if self.non_teaching_female_staff and self.non_teaching_female_staff < 0:
            frappe.throw(
                "Number is negative at Section 10 (non_teaching_female_staff)")

        if self.non_govt_female_teachers and self.non_govt_female_teachers < 0:
            frappe.throw(
                "Number is negative at Section 5 (non_govt_female_teachers)")

        if self.non_govt_female_teachers and self.non_govt_female_teachers < 0:
            frappe.throw(
                "Number is negative at Section 5 (non_govt_female_teachers)")

    def set_school_criteria(self):
        default_year = frappe.db.get_single_value("ASC Panel", "default_year")
        smc_criteria = 'No'
        gsp_criteria = 'No'
        asc_criteria = 'No'

        print("Print from ASC" , default_year)

        if self.year == default_year:
            print("Print from ASC")
            if self.status_detail == 'Functional':
                smc_criteria = 'Yes'
                girls = 0
                if self.school_gender != 'Boys':
                    six_class = frappe.db.sql("Select girls from `tabEnrolment Class and Gender wise` where parent = '%s' and `class` = 'Class-VI' "%(self.name))
                    if six_class :
                        if  six_class[0][0]:
                            girls = girls + six_class[0][0]

                    nine_class = frappe.db.sql("Select SUM(IFNULL(girls,0)) from `tabEnrolment Class and Gender wise` where parent = '%s' and `class` in ('Class-IX Others' , 'Class-IX Arts-General' , 'Class-IX Biology' , 'Class-IX Computer' , 'Class-IX Commerce') "%(self.name))
                    
                    if nine_class:
                        if  nine_class[0][0]:
                            girls = girls + nine_class[0][0]

                    ten_class = frappe.db.sql("Select SUM(IFNULL(girls,0)) from `tabEnrolment Class and Gender wise` where parent = '%s' and `class` in ('Class-X Others' , 'Class-X Arts-General' , 'Class-X Biology' , 'Class-X Computer' , 'Class-X Commerce') "%(self.name))
                    if ten_class:
                        if  ten_class[0][0]:
                            girls = girls + ten_class[0][0]
                    if girls > 0:
                        gsp_criteria = 'Yes'
            enabled = frappe.db.sql("Select enabled from tabSchool where enabled = 1 and name = '%s'"%(self.semis_code))
            if enabled:
                asc_criteria = 'Yes'
            school = frappe.get_doc("School", self.semis_code)
            if len(school.yearly_criteria_history) > 0:
                for row in school.yearly_criteria_history:
                    if row.year == default_year:
                        row.smc_criteria = smc_criteria
                        row.gsp_criteria = gsp_criteria
                        row.asc_criteria = asc_criteria
            else:
                school.append("yearly_criteria_history",{
                    'year' : '2021-22',
                    'smc_criteria' : smc_criteria,
                    'gsp_criteria' : gsp_criteria,
                    'asc_criteria' : asc_criteria,

                })
            

            school.gsp_criteria = gsp_criteria
            school.smc_criteria = smc_criteria
            school.asc_criteria = asc_criteria
            school.save()
    def update_kpi(self):
        frappe.db.sql( """ INSERT INTO `tabASC_KPI` (
        `name`,
        `asc_modified`,
        `modified_by`,
        `semis_code`,
        `year`,
        `only_year`,
        `division`,
        `district`,
        `tehsil`,
        `uc`,
        `na`,
        `ps`,
        `school_name`,
        `location`,
        `gender`,
        `level`,
        `status`,
        `closure_period`,
        `closure_reason`,
        `building_availability`,
        `building_ownership`,
        `building_condition`,
        `rooms`,
        `post_primary`,
        `primary`,
        `ecce`,
        `classrooms`,
        `water`,
        `electricity`,
        `condition_of_boundary_wall`,
        `toilet`,
        `hand_wash`,
        `soap`,
        `mhm_facility`,
        `iscampus`,
        `no_of_merged_schools`,
        `boys_enrollment`,
        `girls_enrollment`,
        `total_enrollment`,
        `sindhi_enrollment`,
        `urdu_enrollment`,
        `english_enrollment`,
        `male_teachers`,
        `female_teachers`,
        `total_teachers`,
        `ecce_male`,
        `ecce_female`,
        `katchi_male`,
        `katchi_female`,
        `class_1_male`,
        `class_1_female`,
        `class_2_male`,
        `class_2_female`,
        `class_3_male`,
        `class_3_female`,
        `class_4_male`,
        `class_4_female`,
        `class_5_male`,
        `class_5_female`,
        `class_6_male`,
        `class_6_female`,
        `class_7_male`,
        `class_7_female`,
        `class_8_male`,
        `class_8_female`,
        `class_9_male`,
        `class_9_female`,
        `class_10_male`,
        `class_10_female`,
        `class_11_male`,
        `class_11_female`,
        `class_12_male`,
        `class_12_female`
        )
        SELECT
        *
        FROM
        (SELECT
        tbl1.name,
        tbl1.modified,
        tbl1.modified_by,
        tbl1.semis_code,
        tbl1.year,
        SUBSTRING( tbl1.year ,1, 4),
        tbl1.region AS `division`,
        tbl1.`district`,
        tbl1.taluka AS `tehsil`,
        tbl1.`uc`,
        tbl1.ena_constituency AS `na`,
        tbl1.fps_constituency AS `ps`,
        tbl1.`school_name`,
        tbl1.`location`,
        tbl1.school_gender AS `gender`,
        tbl1.`level`,
        tbl1.status_detail AS `status`,
        tbl1.`school_duration_of_closure` AS `closure_period`,
        tbl1.`major_reason_closure` AS `closure_reason`,
        tbl1.availability_of_building AS `building_availability`,
        tbl1.yes_relevant_code AS `building_ownership`,
        tbl1.condition_of_building AS `building_condition`,
        tbl1.total_rooms AS `rooms`,
        tbl1.`post_primary`,
        tbl1.`primary`,
        tbl1.`ecce`,
        tbl1.total_rooms_school AS `classrooms`,
        tbl1.water_available AS `water`,
        tbl1.electricity_availability AS `electricity`,
        tbl1.`condition_of_boundary_wall`,
        tbl1.toilet_facility AS `toilet`,
        tbl1.hand_wash_facility AS `hand_wash`,
        tbl1.l_availability_of_soap_at_hand_wash_ AS `soap`,
        tbl1.`mhm_facility`,
        tbl1.is_campus_school AS `iscampus`,
        COALESCE (tbl1.no_of_merger_schools, 0) AS `no_of_merged_schools`,
        tbl1.`male_enrollment` AS boys_enrollment,
        tbl1.`female_enrollment` AS girls_enrollment,
        tbl1.`total_enrollment` AS total_enrollment,
        tbl1.`sindhi_medium_enrolment` AS sindhi_enrollment,
        tbl1.`urdu_medium_enrolment` AS urdu_enrollment,
        tbl1.`english_medium_enrolment` AS english_enrollment,
        (
            tbl1.`govt_male_teachers` + tbl1.`non_govt_male_teachers`
        ) AS male_teachers,
        (
            tbl1.`govt_female_teachers` + tbl1.`non_govt_female_teachers`
        ) AS female_teachers,
        tbl1.total_teacher AS total_teacher,
        SUM(CASE WHEN enrol.class='ECE' THEN enrol.boys ELSE 0 END) AS 'ecce_male',
        SUM(CASE WHEN enrol.class='ECE' THEN enrol.girls ELSE 0 END) AS 'ecce_female',

        SUM(CASE WHEN enrol.class='Katchi' THEN enrol.boys ELSE 0 END) AS 'katchi_male',
        SUM(CASE WHEN enrol.class='Katchi' THEN enrol.girls ELSE 0 END) AS 'katchi_female',

        SUM(CASE WHEN enrol.class='Class-I' THEN enrol.boys ELSE 0 END) AS "class_1_male",
        SUM(CASE WHEN enrol.class='Class-I' THEN enrol.girls ELSE 0 END) AS "class_1_female",

        SUM(CASE WHEN enrol.class='Class-II' THEN enrol.boys ELSE 0 END) AS "class_2_male",
        SUM(CASE WHEN enrol.class='Class-II' THEN enrol.girls ELSE 0 END) AS "class_2_female",

        SUM(CASE WHEN enrol.class='Class-III' THEN enrol.boys ELSE 0 END) AS "class_3_male",
        SUM(CASE WHEN enrol.class='Class-III' THEN enrol.girls ELSE 0 END) AS "class_3_female",

        SUM(CASE WHEN enrol.class='Class-IV' THEN enrol.boys ELSE 0 END) AS "class_4_male",
        SUM(CASE WHEN enrol.class='Class-IV' THEN enrol.girls ELSE 0 END) AS "class_4_female",

        SUM(CASE WHEN enrol.class='Class-V'THEN enrol.boys ELSE 0 END) AS "class_5_male",
        SUM(CASE WHEN enrol.class='Class-V' THEN enrol.girls ELSE 0 END) AS "class_5_female",

        SUM(CASE WHEN enrol.class='Class-VI' THEN enrol.boys ELSE 0 END) AS "class_6_male",
        SUM(CASE WHEN enrol.class='Class-VI' THEN enrol.girls ELSE 0 END) AS "class_6_female",

        SUM(CASE WHEN enrol.class='Class-VII' THEN enrol.boys ELSE 0 END) AS "class_7_male",
        SUM(CASE WHEN enrol.class='Class-VII' THEN enrol.girls ELSE 0 END) AS "class_7_female",

        SUM(CASE WHEN enrol.class='Class-VIII' THEN enrol.boys ELSE 0 END) AS "class_8_male",
        SUM(CASE WHEN enrol.class='Class-VIII' THEN enrol.girls ELSE 0 END) AS "class_8_female",

        SUM(CASE WHEN enrol.class LIKE 'Class-IX%' THEN enrol.boys ELSE 0 END) AS "class_9_male",
        SUM(CASE WHEN enrol.class LIKE 'Class-IX%' THEN enrol.girls ELSE 0 END) AS "class_9_female",

        SUM(CASE WHEN enrol.class LIKE 'Class-X%' THEN enrol.boys ELSE 0 END) AS "class_10_male",
        SUM(CASE WHEN enrol.class LIKE 'Class-X%' THEN enrol.girls ELSE 0 END) AS "class_10_female",

        SUM(CASE WHEN enrol.class LIKE 'Class-XI%' THEN enrol.boys ELSE 0 END) AS "class_11_male",
        SUM(CASE WHEN enrol.class LIKE 'Class-XI%' THEN enrol.girls ELSE 0 END) AS "class_11_female",

        SUM(CASE WHEN enrol.class LIKE 'Class-XI%' THEN enrol.boys ELSE 0 END) AS "class_12_male",
        SUM(CASE WHEN enrol.class LIKE 'Class-XI%' THEN enrol.girls ELSE 0 END) AS "class_12_female"
        FROM
        `tabASC` AS tbl1  
        LEFT JOIN `tabEnrolment Class and Gender wise` AS enrol
            ON enrol.parent = tbl1.name where tbl1.name = '{}' and tbl1.docstatus != 2
        GROUP BY tbl1.name) AS maintbl
        ON DUPLICATE KEY
        UPDATE
        `asc_modified` = maintbl.modified,
        modified_by = maintbl.modified_by,
        semis_code = maintbl.semis_code,
        `year` = maintbl.year,
        `only_year` = SUBSTRING(maintbl.year,1, 4),
        `division` = maintbl.division,
        `district` = maintbl.district,
        `tehsil` = maintbl.tehsil,
        `uc` = maintbl.uc,
        `na` = maintbl.na,
        `ps` = maintbl.ps,
        `school_name` = maintbl.school_name,
        `location` = maintbl.location,
        `gender` = maintbl.gender,
        `level` = maintbl.level,
        `status` = maintbl.status,
        `closure_period` = maintbl.closure_period,
        `closure_reason` = maintbl.closure_reason,
        `building_availability` = maintbl.building_availability,
        `building_ownership` = maintbl.building_ownership,
        `building_condition` = maintbl.building_condition,
        `rooms` = maintbl.rooms,
        `post_primary` = maintbl.post_primary,
        `primary` = maintbl.primary,
        `ecce` = maintbl.ecce,
        `classrooms` = maintbl.classrooms,
        `water` = maintbl.water,
        `electricity` = maintbl.electricity,
        `condition_of_boundary_wall` = maintbl.condition_of_boundary_wall,
        `toilet` = maintbl.toilet,
        `hand_wash` = maintbl.hand_wash,
        `soap` = maintbl.soap,
        `mhm_facility` = maintbl.mhm_facility,
        `iscampus` = maintbl.iscampus,
        `no_of_merged_schools` = maintbl.no_of_merged_schools,
        `boys_enrollment` = maintbl.boys_enrollment,
        `girls_enrollment` = maintbl.girls_enrollment,
        `total_enrollment` = maintbl.total_enrollment,
        `sindhi_enrollment` = maintbl.sindhi_enrollment,
        `urdu_enrollment` = maintbl.urdu_enrollment,
        `english_enrollment` = maintbl.english_enrollment,
        `male_teachers` = maintbl.male_teachers,
        `female_teachers` = maintbl.female_teachers,
        `total_teachers` = maintbl.total_teacher,
        `ecce_male` = maintbl.ecce_male,
        `ecce_female` = maintbl.ecce_female,
        `katchi_male` = maintbl.katchi_male,
        `katchi_female` = maintbl.katchi_female,
        `class_1_male` = maintbl.class_1_male,
        `class_1_female` = maintbl.class_1_female,
        `class_2_male` = maintbl.class_2_male,
        `class_2_female` = maintbl.class_2_female,
        `class_3_male` = maintbl.class_3_male,
        `class_3_female` = maintbl.class_3_female,
        `class_4_male` = maintbl.class_4_male,
        `class_4_female` = maintbl.class_4_female,
        `class_5_male` = maintbl.class_5_male,
        `class_5_female` = maintbl.class_5_female,
        `class_6_male` = maintbl.class_6_male,
        `class_6_female` = maintbl.class_6_female,
        `class_7_male` = maintbl.class_7_male,
        `class_7_female` = maintbl.class_7_female,
        `class_8_male` = maintbl.class_8_male,
        `class_8_female` = maintbl.class_8_female,
        `class_9_male` = maintbl.class_9_male,
        `class_9_female` = maintbl.class_9_female,
        `class_10_male` = maintbl.class_10_male,
        `class_10_female` = maintbl.class_10_female,
        `class_11_male` = maintbl.class_11_male,
        `class_11_female` = maintbl.class_11_female,
        `class_12_male` = maintbl.class_12_male,
        `class_12_female` = maintbl.class_12_female """.format(self.name))









@frappe.whitelist()
def share_semis_code(semis_code=None, district=None, main_semis=None):
    return_name = ""
    if district and semis_code and main_semis:
        shared_semis_code = frappe.db.sql(
            """ select name,IFNULL(school_name, " ") from `tabSchool` where district = %s and name=%s and name!=%s """, (district, semis_code, main_semis))
        if shared_semis_code:
            return_name = shared_semis_code[0][1]
            return 0, return_name
        else:
            return 1, return_name


@frappe.whitelist()
def get_defaults():
    reference_date = frappe.db.get_single_value(
        "ASC Panel", "reference_date")
    default_year = frappe.db.get_single_value("ASC Panel", "default_year")
    date_time = frappe.utils.now()
    return [reference_date, default_year, date_time]


@frappe.whitelist()
def select_values():
    school_administration = frappe.db.sql(
        """select name from `tabSchool administration` order by list_order""")
    school_gender = frappe.db.sql(
        """select name from `tabSchool Gender` order by list_order""")
    source_information_closure = frappe.db.sql(
        """select name from `tabSource of information of closure of School` order by list_order""")
    major_reason_closure = frappe.db.sql(
        """select name from `tabWrite major reason for closure` order by list_order""")
    yes_relevant_code = frappe.db.sql(
        """select name from `tabCase In Availability of Building` order by list_order""")
    type_of_building = frappe.db.sql(
        """select name from `tabType of building` order by list_order""")
    condition_of_building = frappe.db.sql(
        """select name from `tabCondition of Building` order by list_order""")
    provision_drinking_water = frappe.db.sql(
        """select name from `tabMode of provision of Drinking Water` order by list_order""")
    construction_work_planned_completed = frappe.db.sql(
        """select name from `tabconstruction work planned` order by list_order""")
    designation = frappe.db.sql(
        """select name from `tabDesignation` order by name""")

    ret = {
        'school_administration': school_administration,
        'school_gender': school_gender,
        'source_information_closure': source_information_closure,
        'major_reason_closure': major_reason_closure,
        'yes_relevant_code': yes_relevant_code,
        'type_of_building': type_of_building,
        'condition_of_building': condition_of_building,
        'provision_drinking_water': provision_drinking_water,
        'construction_work_planned_completed': construction_work_planned_completed,
        'principal_designation': designation,
        'designation_enumerator': designation,
        'designation_education_officer': designation
    }
    return ret


@frappe.whitelist()
def check_roster(semis_code=None):
    return_name = 0
    if not "System Manager" in frappe.get_roles(frappe.session.user):
        if ("Data Entry Operator" in frappe.get_roles(frappe.session.user)):
            shared_semis_code = frappe.db.sql(
                """ select sp.name from `tabSchool Permission` as sp, `tabASC Roster` as ar where sp.parent=ar.name and sp.school = %s and ar.user=%s """, (semis_code, frappe.session.user))
            if not shared_semis_code:
                return_name = 1
    return return_name


@frappe.whitelist()
def level_wise_enrollment():
    enrolment_ = frappe.db.sql(
        """select program_name from `tabProgram` order by order_no""", as_dict=1)
    repeaters_ = frappe.db.sql(
        """select program_name from `tabProgram` where class>=4 and class<=10  order by order_no""", as_dict=1)
    item_ = frappe.db.sql("""select name1 from `tabItem`  """, as_dict=1)

    data = {
        'enrolment': enrolment_,
        'repeaters': repeaters_,
        'item': item_,
    }
    return data


@frappe.whitelist()
def get_merged_schools(semis_code=None):
    enrolment_ = []
    if semis_code:
        enrolment_ = frappe.db.sql(
            """select semis_code, school_name from `tabMerged Schools in Campus` where parent=%s order by semis_code""", (semis_code), as_dict=1)

    data = {
        'enrolment': enrolment_,
        'length_': len(enrolment_),
    }
    return data


@frappe.whitelist()
def get_user_detail():
    return frappe.db.sql("""select first_name, IFNULL(district, "") from `tabUser` where enabled=1 and name=%s """, (frappe.session.user))


