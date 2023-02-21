import frappe
import re


@frappe.whitelist()
def get_data():
    temp_query = """ Select Distinct(semis_code) as "SEMIS Code", district as "District", taluka as "Tehsil",
                uc as "UC", ena_constituency as "NA", fps_constituency as "PS", school_name as "School Name", 
                location "Location", school_gender as "Gender",
                level as "Level", status_detail as "Status", school_duration_of_closure as "Closure Period",
                major_reason_closure as "Closure Reason", availability_of_building as "Building Availability", yes_relevant_code as "Building Ownership",
                condition_of_building as "Building Condition", total_rooms_school as "Rooms", total_rooms as "Classrooms", water_available as "Water"
                ,electricity_connection as "Electricity"
                ,condition_of_boundary_wall "Condition of Boundary Wall",toilet_facility as "Toilet",hand_wash_facility as "Hand Wash"
                ,is_campus_school as "isCampus", no_of_merger_schools as "No. of Merged Schools",
                SUM(enrol.boys) as "Boys Enrollment",
                SUM(enrol.girls) as "Girls Enrollment",
                SUM(enrol.boys + enrol.girls) as "Total Enrollment",
                sindhi_medium_enrolment as "Sindhi Enrollment", 
                urdu_medium_enrolment as "Urdu Enrollment",
                english_medium_enrolment as "English Enrollment" ,
                (govt_male_teachers + non_govt_male_teachers) as "Male Teachers",
                (govt_female_teachers + non_govt_female_teachers) as "Female Teachers", 
                (govt_male_teachers + non_govt_male_teachers+govt_female_teachers + non_govt_female_teachers) as "Total Teachers"
                from tabASC 
                left join 
                (Select * from `tabEnrolment Class and Gender wise` where parent like '%2021-22') enrol on tabASC.name = enrol.parent
                 where year = '2021-22' and district = "Badin"
                and tabASC.docstatus != 2
                group by semis_code LIMIT 1,10""" 
    data = frappe.db.sql(temp_query,as_dict=1)
    return data
