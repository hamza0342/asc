import frappe
import json

@frappe.whitelist()
def get_data(year = None, division = None,gender=None,transition_type=None):
    case_string=""
    division_case_string=""
    if division:
        case_string=" and region = '%s' " %(str(division))
        division_case_string= " and k.division = '%s' " %(str(division))

    class_case_string,prevyear= get_case_string(year,gender,transition_type)
    
    
    #SUM(CASE WHEN `year` = CONCAT('%s','-','%s') THEN class_5_female ELSE 0 END) prev_5_female,
	#SUM(CASE WHEN `year` = CONCAT('%s','-','%s') THEN class_5_male ELSE 0 END) prev_5_male,
	#SUM(CASE WHEN `year` = '%s' THEN class_6_female ELSE 0 END) cur_6_female,
	#SUM(CASE WHEN `year` = '%s' THEN class_6_male ELSE 0 END) cur_6_male,
    #SUM(CASE WHEN k.`year` = CONCAT('%s','-','%s') THEN (k.class_5_male+k.class_5_female) ELSE 0 END) prev_5,
    #SUM(CASE WHEN k.`year` = '%s' THEN (k.class_6_male+k.class_6_female) ELSE 0 END) cur_6     
    
    
    temp_query = """Select k.district as name, %s
    ,  
    d.path_features as path
    from tabASC_KPI k
    Left join 
    tabDistrict d 
    on 
    k.district = d.name where k.district != 'Keamari Karachi'   %s 
    group by k.district"""%(class_case_string,division_case_string) 
    # frappe.msgprint(temp_query)
    
    data = frappe.db.sql(temp_query, as_dict=1)  

    # data = sorted(data, key=lambda x: x['value'], reverse=True)
    

    data_ =[]
    data_.append(data)
    data_.append(prevyear)

    return data_


def get_case_string(year,gender,transition_type):
    year_ = int(year[:4])

    prev_year = frappe.db.sql(""" Select only_year from tabASC_KPI where only_year < %s order by only_year desc limit 1 """%(year_))[0][0]
    if transition_type == "Primary to Post Primary":
        if gender == "Boys":
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_6_male) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_5_male) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
        elif gender == "Girls":
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_6_female) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_5_female) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
        else:
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_6_male+k.class_6_female) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_5_male+k.class_5_female) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
    elif transition_type == "Middle to Secondary":
        if gender == "Boys":
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_9_male) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_8_male) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
        elif gender == "Girls":
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_9_female) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_8_female) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
        else:
            class_case_string = """ ROUND(SUM(CASE WHEN k.`only_year` = %s THEN (k.class_9_male+k.class_9_female) ELSE 0 END)
            /
            SUM(CASE WHEN k.`only_year` =%s THEN (k.class_8_male+k.class_8_female) ELSE 0 END)*100,2) as value"""%(year_,prev_year)
    return class_case_string, str(year_)+str(year_+1)[2:]