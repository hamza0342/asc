import frappe
import json

@frappe.whitelist()
def get_data(basic_facility = None, year = None, division = None):
    facility = basic_facility
    # frappe.msgprint(facility)

    case_string=""
    division_case_string=""
    if division:
        case_string=" and region = '%s' " %(str(division))
        division_case_string= " and k.division = '%s' " %(str(division))
    facility_name = get_facility(facility,year)

    temp_query = """Select k.district as name,
     %s , 
    d.path_features as path
    from tabASC_KPI k
    Left join 
    tabDistrict d 
    on 
    k.district = d.name where Year = '%s' and status = 'Functional' %s and k.district != 'Keamari Karachi' group by k.district """%(facility_name,str(year),division_case_string)
    # frappe.msgprint(frappe.as_json(temp_query))
    
    data = frappe.db.sql(temp_query, as_dict=1)
    # frappe.msgprint(frappe.as_json(data))
    data = sorted(data, key=lambda x: x['value'], reverse=True)
    # frappe.msgprint(frappe.as_json(data))




    return data



def get_facility(facility,year):
    query = ""
    if facility == "ECCE Enrollment":
        query = """COUNT(k.name) AS Total_Schools , 
         IFNULL(SUM(CASE WHEN ( (IFNULL(`ecce_male`,0)+ IFNULL(`ecce_female`,0)) >0) THEN 1 ELSE 0 END),0) as facility_available,
         IFNULL(SUM(CASE WHEN ( (IFNULL(`ecce_male`,0)+ IFNULL(`ecce_female`,0)) >0) THEN (IFNULL(`ecce_male`,0) + IFNULL(`ecce_female`,0)) ELSE 0 END),0) as ecce_enrollment , 
         ROUND( IFNULL(SUM(CASE WHEN ( (IFNULL(`ecce_male`,0)+ IFNULL(`ecce_female`,0)) >0) THEN 1 ELSE 0 END),0)  / count(k.name)  *100 , 1 ) as value"""
    elif facility == "ECCE Rooms":
        query = """COUNT(k.name) AS Total_Schools, 
        IFNULL(SUM(if((IFNULL(`ecce`,0)) > 0  , 1, 0)),0) as facility_available , 
        IFNULL(SUM(CASE WHEN ( (IFNULL(`ecce_male`,0)+ IFNULL(`ecce_female`,0)) >0) THEN (IFNULL(`ecce_male`,0) + IFNULL(`ecce_female`,0)) ELSE 0 END),0) as ecce_enrollment , 
        ROUND(IFNULL(SUM(if((IFNULL(`ecce`,0)) > 0  , 1, 0)),0) / count(k.name) *100 , 1 ) as value"""
    # frappe.msgprint(facility)
    # frappe.msgprint(query)

    return query
