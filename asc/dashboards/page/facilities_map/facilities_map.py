import frappe
import json

@frappe.whitelist()
def get_data(basic_facility = None, year = None, division = None):
    facility = basic_facility
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
    k.district = d.name where k.district != 'Keamari Karachi' and Year = '%s' %s group by k.district"""%(facility_name,str(year),division_case_string)
    # frappe.msgprint(frappe.as_json(temp_query))
    
    data = frappe.db.sql(temp_query, as_dict=1) 
#     frappe.msgprint(frappe.as_json(data))

    data = sorted(data, key=lambda x: x['value'], reverse=True)
    # frappe.msgprint(frappe.as_json((basic_facility.replace(" ","_")).lower()))

    color_query = """Select `min` as 'from', (CASE WHEN `max`= 0 then '' else `max` end) as 'to' , `color` as 'color' , `range` as 'name' from `tabColor Indication` where parentfield = '%s' order by `order` asc"""%((basic_facility.replace(" ","_")).lower())
    color_data =  frappe.db.sql(color_query, as_dict=1)  
    for row in color_data:
        if row['to'] == '':
            del row['to']
    data_ =[]
    data_.append(data) 
    data_.append(color_data)

    return data_



def get_facility(facility,year):
    query = ""
    if facility == "Toilet":
        query = "COUNT(k.name) AS Total_Schools , IFNULL(SUM(CASE WHEN toilet ='Yes' THEN 1 ELSE 0 END),0)  as facility_available, ROUND(IFNULL(SUM(CASE WHEN toilet ='Yes' THEN 1 ELSE 0 END),0) / count(k.name) *100 ,1) as value"
    elif facility == "Drinking Water":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(if(water = 'Yes'  , 1, 0)),0) as facility_available ,  ROUND(IFNULL(SUM(if(water = 'Yes'  , 1, 0)),0) / count(k.name) *100 ,1) as value"
    elif facility == "Electricity":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(if(electricity = 'No Electricity Connection' OR electricity='' OR electricity IS NULL,0,1)),0) as facility_available ,ROUND(IFNULL(SUM(if(electricity = 'No Electricity Connection' OR electricity='' OR electricity IS NULL,0,1)),0) / count(k.name) *100 ,1)as value  "
    elif facility == "Building":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(CASE WHEN `building_availability`='Yes' THEN 1 ELSE 0 END),0) as facility_available, ROUND(IFNULL(SUM(CASE WHEN `building_availability`='Yes' THEN 1 ELSE 0 END),0) / count(k.name) *100 ,1)as value "
    elif facility == "Boundary Wall":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(if(`condition_of_boundary_wall`='No Boundary Wall' OR `condition_of_boundary_wall`='' OR `condition_of_boundary_wall` IS NULL, 0, 1) ),0) as facility_available, ROUND(IFNULL(SUM(if(`condition_of_boundary_wall`='No Boundary Wall' OR `condition_of_boundary_wall`='' OR `condition_of_boundary_wall` IS NULL, 0, 1) ),0) / count(k.name) *100 ,1)as value "
    elif facility == "Hand Wash":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(if(`hand_wash`='Yes', 1, 0) ),0) as facility_available, ROUND(IFNULL(SUM(if(`hand_wash`='Yes', 1, 0) ),0)  / count(k.name) *100,1) as value   "
    elif facility == "Soap":
        query = "COUNT(k.name) AS Total_Schools, IFNULL(SUM(if(`soap`='Yes', 1, 0) ),0) as facility_available, ROUND(IFNULL(SUM(if(`soap`='Yes', 1, 0) ),0)  / count(k.name) *100 ,1) as value   "
    elif facility == "MHM Disposal":
        query = "SUM(CASE WHEN gender != 'Boys' and level != 'Primary' and Year = '%s' then 1 else 0 end) AS Total_Schools, IFNULL(SUM(if(`mhm_facility`='Yes', 1, 0) ),0) as facility_available, ROUND(IFNULL(SUM(if(`mhm_facility`='Yes', 1, 0) ),0)  / SUM(CASE WHEN gender != 'Boys' and level != 'Primary' and Year = '%s' then 1 else 0 end) *100 ,1) as value   "%(year,year)
    return query


@frappe.whitelist()
def get_taluka_data(basic_facility = None, year = None, district = None):

    facility = basic_facility
    case_string=""
    division_case_string=""
    if district:
        division_case_string= " and k.district = '%s' " %(str(district))
    facility_name = get_facility(facility,year)


    temp_query = """Select k.district as name,
     Count(k.name) as total_schools , 
     Sum(Case when status = 'Functional' then 1 else 0 end ) as funcional,
     Sum(Case when status = 'Closed' then 1 else 0 end ) as closed,

     Sum(Case when gender = 'Boys' then 1 else 0 end ) as boys,
     Sum(Case when gender = 'Girls' then 1 else 0 end ) as girls,
     Sum(Case when gender = 'Mixed' then 1 else 0 end ) as mixed,

     Sum(Case when level = 'Primary' then 1 else 0 end ) as 'primary',
     Sum(Case when level = 'Elementary' then 1 else 0 end ) as elementry,
     Sum(Case when level = 'Middle' then 1 else 0 end ) as middle,
     Sum(Case when level = 'Secondary' then 1 else 0 end ) as secondary,
     Sum(Case when level = 'Higher Secondary' then 1 else 0 end ) as higher_secondary,

     SUM( IFNULL(`boys_enrollment`,0)) as male_enrollment,
     SUM( IFNULL(`girls_enrollment`,0)) as female_enrollment,
     SUM(IFNULL(`male_teachers`,0)) as male_teachers,
     SUM(IFNULL(`female_teachers`,0)) as female_teachers,

     SUM(if(water = 'Yes'  , 1, 0)) as water,
     SUM(if(`condition_of_boundary_wall`='No Boundary Wall' OR `condition_of_boundary_wall`='' OR `condition_of_boundary_wall` IS NULL, 0, 1) ) as boundary_wall,
     SUM(if(`hand_wash`='Yes', 1, 0) ) as hand_wash,
     SUM(if(`mhm_facility`='Yes', 1, 0) ) as mhm,
     SUM(CASE WHEN gender != 'Boys' and level != 'Primary'  then 1 else 0 end) AS total_mhm_Schools,
     SUM(CASE WHEN `building_availability`='Yes' THEN 1 ELSE 0 END) as building,
     SUM(CASE WHEN toilet ='Yes' THEN 1 ELSE 0 END) as toilet,
     SUM(if(electricity = 'No Electricity Connection' OR electricity='' OR electricity IS NULL,0,1)) as electricity,
     SUM(if(`soap`='Yes', 1, 0) ) as soap

    from tabASC_KPI k
     where Year = '%s'  %s """%(str(year),division_case_string)
    # frappe.msgprint(frappe.as_json(temp_query))
    
    data_ = frappe.db.sql(temp_query, as_dict=1) 

    if data_[0]['total_schools']:
        if data_[0]['primary']:
            data_[0]['primary_percentage'] = round(data_[0]['primary'] / data_[0]['total_schools'] * 100,1)
        else:
            data_[0]['primary_percentage'] = 0
        if data_[0]['elementry']:
                data_[0]['elementry_percentage'] = round(data_[0]['elementry'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['elementry_percentage'] = 0
        if data_[0]['middle']:
                data_[0]['middle_percentage'] = round(data_[0]['middle'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['middle_percentage'] = 0       
        if data_[0]['secondary']:
                data_[0]['secondary_percentage'] = round(data_[0]['secondary'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['secondary_percentage'] = 0 
        if data_[0]['higher_secondary']:
                data_[0]['higher_secondary_percentage'] = round(data_[0]['higher_secondary'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['higher_secondary_percentage'] = 0 
        if data_[0]['water']:
                data_[0]['water_percentage'] = round(data_[0]['water'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['water_percentage'] = 0 
        if data_[0]['boundary_wall']:
                data_[0]['boundary_wall_percentage'] = round(data_[0]['boundary_wall'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['boundary_wall_percentage'] = 0 
        if data_[0]['hand_wash']:
                data_[0]['hand_wash_percentage'] = round(data_[0]['hand_wash'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['hand_wash_percentage'] = 0 
        if data_[0]['mhm'] and data_[0]['total_mhm_Schools']:
                data_[0]['mhm_percentage'] = round(data_[0]['mhm'] / data_[0]['total_mhm_Schools'] * 100,1)
        else:
                data_[0]['mhm_percentage'] = 0 
        if data_[0]['building'] :
                data_[0]['building_percentage'] = round(data_[0]['building'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['building_percentage'] = 0 
        if data_[0]['toilet'] :
                data_[0]['toilet_percentage'] = round(data_[0]['toilet'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['toilet_percentage'] = 0 
        if data_[0]['electricity'] :
                data_[0]['electricity_percentage'] = round(data_[0]['electricity'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['electricity_percentage'] = 0
        if data_[0]['soap'] :
                data_[0]['soap_percentage'] = round(data_[0]['soap'] / data_[0]['total_schools'] * 100,1)
        else:
                data_[0]['soap_percentage'] = 0
    # return_data={'District': data}

    temp_query_ = """Select k.tehsil as name,
     %s , 
    d.path_features as path
    from tabASC_KPI k
    Left join 
    tabDistrict d 
    on 
    k.district = d.name where Year = '%s' %s group by k.tehsil"""%(facility_name,str(year),division_case_string)
    # frappe.msgprint(frappe.as_json(temp_query_))
    
    data = frappe.db.sql(temp_query_, as_dict=1) 
    data = sorted(data, key=lambda x: x['value'], reverse=True)
    return_data={'District': data_,
                'Taluka': data}

    return return_data

