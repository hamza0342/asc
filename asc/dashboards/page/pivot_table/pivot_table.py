from socketserver import ThreadingUnixDatagramServer
import frappe
import json
 
@frappe.whitelist()
def get_data(year=None,five_years=None,ctype=None):
    cond = ''
    if five_years == '1':
        years = frappe.db.sql("Select name from tabYear  order by name DESC limit 5",as_dict = 1)
        if years:
            years_t = []
            for year in years:
                years_t.append(year['name'])
            years_t = tuple(years_t)
            cond+= " where year in {} ".format(years_t)
    else:
        cond+= " where year= '%s' "%(year)
    temp_query = """SELECT 
                    `name` as id,
                    `semis_code` as  "SEMIS Code",
                    `year` as  "Year",
                    `division` as "Division",
                    `district` as  "District",
                    `tehsil` as "Tehsil",
                    `uc` as "UC",
                    `na` as "NA",
                    `ps` as "PS",
                    `school_name` as "School Name",
                    `location` as "Location",
                    `gender` as "Gender",
                    `level` as "Level",
                    `status` as "Status",
                    `closure_period` as "Closure Period",
                    `closure_reason` as "Closure Reason",
                    `building_availability` as "Building Availability",
                    `building_ownership` as "Building Ownership",
                    `building_condition` as "Building Condition",
                    `rooms` as "Rooms",
                    `post_primary` as "Post Primary",
                    `primary` as "Primary",
                    `ecce` as "ECCE",
                    `classrooms` as "Classrooms" ,
                    `water` as "Water",
                    `electricity` as "Electricity",
                    `condition_of_boundary_wall` as "Condition of Boundary Wall",
                    `toilet` as "Toilet",
                    `hand_wash` as "Hand Wash",
                    `soap` as "Soap",
                    `mhm_facility` as "MHM Facility",
                    `iscampus` as "Campus",
                    `no_of_merged_schools` as "No. of Merged Schools",
                    `boys_enrollment` as "Boys Enrollment",
                    `girls_enrollment` as "Girls Enrollment",
                    `total_enrollment` as "Total Enrollment",
                    `sindhi_enrollment` as "Sindhi Enrollment",
                    `urdu_enrollment` as "Urdu Enrollment",
                    `english_enrollment` as "English Enrollment",
                    `male_teachers` as "Male Teachers",
                    `female_teachers` as "Female Teachers",
                    `total_teachers` as "Total Teachers",
                    `ecce_male` as "ECCE Male",
                    `ecce_female` as "ECCE Female",
                    `katchi_male` as "Katchi Male",
                    `katchi_female` as "Katchi Female",
                    `class_1_male`  as "Class-I Male", 
                    `class_1_female` as "Class-I Female",
                    `class_2_male` as "Class-II Male",
                    `class_2_female` as "Class-II Female",
                    `class_3_male` as "Class-III Male",
                    `class_3_female` as "Class-III Female",
                    `class_4_male` as "Class-IV Male",
                    `class_4_female` as "Class-IV Female",
                    `class_5_male` as "Class-V Male",
                    `class_5_female` as "Class-V Female",
                    `class_6_male` as "Class-VI Male",
                    `class_6_female` as "Class-VI Female",
                    `class_7_male` as "Class-VII Male",
                    `class_7_female` as "Class-VII Female",
                    `class_8_male` as "Class-VIII Male",
                    `class_8_female` as "Class-VIII Female",
                    `class_9_male` as "Class-IX Male",
                    `class_9_female` as "Class-IX Female",
                    `class_10_male` as "Class-X Male",
                    `class_10_female` as "Class-X Female",
                    `class_11_male` as "Class-XI Male",
                    `class_11_female` as "Class-XI Female",
                    `class_12_male` as "Class-XII Male",
                    `class_12_female` as "Class-XII Female"  FROM tabASC_KPI %s """%(cond) 
    data = frappe.db.sql(temp_query,as_dict=1)
    return data


@frappe.whitelist()
def save_data(report_name=None,option=None,current_user=None,year=None,last_five_years=None,pivot_options=None,pivot_columns=None):
    obj = frappe.new_doc("Pivot Table Data")
    obj.report_name = report_name
    obj.status=option
    obj.user= current_user
    obj.year= year
    obj.last_five_years= last_five_years
    obj.pivot_options= pivot_options
    obj.pivot_columns=pivot_columns
    obj.save(ignore_permissions=True)
    return 1



@frappe.whitelist()
def report_names(current_user = None):
    names = frappe.db.sql("Select name from `tabPivot Table Data` where status = 'Public' or user = '%s'"%(current_user))
    if names:
        result =[]
        for n in names:
            result.append(n[0])
        return result
    else:
        return ["No report"]

@frappe.whitelist()
def get_report(report_name=None):
    result = []
    obj = frappe.get_doc("Pivot Table Data",report_name)
    result.append(obj.pivot_options) 
    result.append(obj.pivot_columns)
    data_source={"year":obj.year, "last_five_years":obj.last_five_years}
    result.append(data_source)
    return result