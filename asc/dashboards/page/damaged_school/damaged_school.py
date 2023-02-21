import frappe
@frappe.whitelist()
def get_data(basic_facility = None, year = None, division = None, district = None):
    condition = " and tac.year= '%s' " % str(year)
    if division:
        condition += " and tac.region= '%s' " % str(division)
    if district:
        condition += " and tac.district= '%s' " % str(district) 
        if basic_facility=='Fully Damaged':
             condition += " and tabimage.fully= 'Yes' "
         
        if basic_facility=='Partially Damaged':
             condition += " and tabimage.partially= 'Yes' " 
            
        if basic_facility=='School Converted in IDP':
             condition += " and tabimage.school_converted_in_idp_camps= 'Yes' "
     

    if district:
        data_ = frappe.db.sql("""SELECT   tac.semis_code as semiscode,tac.year, tac.name,tabimage.name as floodname,tabimage.fully, tabimage.partially, tabimage.school_converted_in_idp_camps, tabimage.population_accomodated, tabimage.no_of_families, tabimage.semis_code, tabimage.`school_name` as School_name, tabimage.`district`,case when tabimage.`lat` is null then tac.`lat_n` ELSE tabimage.`lat` END as lat ,case when tabimage.`lag` is null then tac.`lon_e` ELSE tabimage.`lag` END as lng, IFNULL(tac.level, "-") AS level, IFNULL(tac.school_gender,"-") AS school_gender  FROM `tabFlood School` as tabimage INNER JOIN tabASC tac ON tabimage.semis_code = tac.semis_code AND tabimage.year = tac.year  where tabimage.docstatus!=2 and (tabimage.`lat` BETWEEN 24 AND 30 OR tac.`lat_n` BETWEEN 24 AND 30) and (tabimage.`lag` BETWEEN 66 AND 72 OR tac.`lon_e` BETWEEN 66 AND 72) %s group by tabimage.semis_code """% (condition), as_dict=1)
    else:
        # data_ = frappe.db.sql("""SELECT tabimage.district as name, COUNT(tac.semis_code) as value, d.path_features as path  FROM `tabFlood School` as tabimage INNER JOIN tabASC tac ON tabimage.semis_code = tac.semis_code AND tabimage.year = tac.year Left join tabDistrict d   on  tabimage.district = d.name  where tabimage.docstatus!=2 %s group by tabimage.district """% (condition), as_dict=1) 
        if basic_facility=='Fully Damaged':
            data_ = frappe.db.sql("""SELECT tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district """% (condition), as_dict=1) 
        elif basic_facility=='Partially Damaged':
            data_ = frappe.db.sql("""SELECT tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where  tac.district != 'Keamari Karachi' AND tac.docstatus!=2 %s group by tac.district """% (condition), as_dict=1)
        elif basic_facility=='School Converted in IDP':
            data_ = frappe.db.sql("""SELECT tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where  tac.district != 'Keamari Karachi' AND tac.docstatus!=2 %s group by tac.district """% (condition), as_dict=1) 
        else:    
            data_ = frappe.db.sql("""SELECT tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN LOWER(tabimage.fully)='yes' OR LOWER(tabimage.partially)='yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN LOWER(tabimage.fully)='yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN LOWER(tabimage.partially)='yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where  tac.district != 'Keamari Karachi' AND tac.docstatus!=2 %s group by tac.district """% (condition), as_dict=1)
        
    #frappe.throw("""SELECT tac.district as name, COUNT(tac.semis_code) as value, d.path_features as path  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.district  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district """% (condition));
    return data_

   
@frappe.whitelist()
def get_districts(district = None):
    condition =""
    if district:
        condition += " and d.name= '%s' " % str(district)
    data_ = frappe.db.sql("""SELECT 
                        d.name as value,
                        d.code,
                        d.type, 
                        d.coordinates
                        FROM `tabDistrict` as d 
                        where name != '' %s 
                        group by d.name 
                        """% (condition), as_dict=1)
    return data_
    
    
@frappe.whitelist()  
def get_schools_data(basic_facility = None, year = None, division = None, district = None):
    condition = " and tac.year= '%s' " % str(year)
    if division:
        condition += " and tac.region= '%s' " % str(division)
    if district:
        condition += " and tac.district= '%s' " % str(district) 
        if basic_facility=='Fully Damaged':
                condition += " and tabimage.fully= 'Yes' " 
            
        if basic_facility=='Partially Damaged':
                condition += " and tabimage.partially= 'Yes' "
            
        if basic_facility=='School Converted in IDP':
                condition += " and tabimage.school_converted_in_idp_camps= 'Yes' "

    data_ = frappe.db.sql("""SELECT   tac.semis_code as semiscode,tac.year, tac.name,tabimage.name as floodname,tabimage.fully, tabimage.partially, tabimage.school_converted_in_idp_camps, tabimage.population_accomodated, tabimage.no_of_families, tabimage.semis_code, tabimage.`school_name` as School_name, tabimage.`district`,case when tabimage.`lat` is null or tabimage.`lat` NOT BETWEEN 24 AND 30 then tac.`lat_n` ELSE tabimage.`lat` END as lat ,case when tabimage.`lag` is null OR tabimage.`lag` NOT BETWEEN 66 AND 72 then tac.`lon_e` ELSE tabimage.`lag` END as lng, IFNULL(tac.level, "-") AS level, IFNULL(tac.school_gender,"-") AS school_gender  FROM `tabFlood School` as tabimage INNER JOIN tabASC tac ON tabimage.semis_code = tac.semis_code AND tabimage.year = tac.year  where tabimage.docstatus!=2 and (tabimage.`lat` IS NOT NULL OR tac.`lat_n`  IS NOT NULL) and (tabimage.`lat` BETWEEN 24 AND 30 OR tac.`lat_n` BETWEEN 24 AND 30) and (tabimage.`lag` BETWEEN 66 AND 72 OR tac.`lon_e` BETWEEN 66 AND 72) %s group by tabimage.semis_code """% (condition), as_dict=1)

    return data_

   
@frappe.whitelist()    
def get_data_charts(basic_facility = None, year = None, division = None, district = None):
    condition = " and tac.year= '%s' " % str(year)
    if division:
        condition += " and tac.region= '%s' " % str(division)
    if district:
        condition += " and tac.district= '%s' " % str(district)  

    if basic_facility=='Fully Damaged':
        data_ = frappe.db.sql("""SELECT tac.region as region,tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path, d.area_of_district as area, ROUND(d.maximum_flood_water_extent,0) as under_water, ROUND(d.total_population_in_district,0) as papulation, ROUND(d.population_potentially_exposed,0) as exposed_papulation, ROUND(d.population_exposed,0) as exposed_papulation_percent FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district ORDER BY tac.region,tac.district ASC """% (condition), as_dict=1) 
    elif basic_facility=='Partially Damaged':
        data_ = frappe.db.sql("""SELECT tac.region as region,tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path , d.area_of_district as area, ROUND(d.maximum_flood_water_extent,0) as under_water, ROUND(d.total_population_in_district,0) as papulation, ROUND(d.population_potentially_exposed,0) as exposed_papulation, ROUND(d.population_exposed,0) as exposed_papulation_percent FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district ORDER BY tac.region,tac.district ASC """% (condition), as_dict=1)
    elif basic_facility=='School Converted in IDP':
        data_ = frappe.db.sql("""SELECT tac.region as region,tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path , d.area_of_district as area, ROUND(d.maximum_flood_water_extent,0) as under_water, ROUND(d.total_population_in_district,0) as papulation, ROUND(d.population_potentially_exposed,0) as exposed_papulation, ROUND(d.population_exposed,0) as exposed_papulation_percent  FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district  ORDER BY tac.region,tac.district ASC """% (condition), as_dict=1) 
    else:    
        data_ = frappe.db.sql("""SELECT tac.region as region,tac.district as name,SUM(tabimage.population_accomodated) as population_accomodated, SUM(tabimage.no_of_families) as no_of_families, COUNT(tac.semis_code) as totalschool, COUNT(CASE WHEN LOWER(tabimage.fully)='yes' OR LOWER(tabimage.partially)='yes' THEN tabimage.semis_code END) as value, COUNT(CASE WHEN tabimage.fully='Yes' THEN tabimage.semis_code END) as fulvalue, COUNT(CASE WHEN tabimage.partially='Yes' THEN tabimage.semis_code END) as parvalue, COUNT(CASE WHEN tabimage.school_converted_in_idp_camps='Yes' THEN tabimage.semis_code END) as idpvalue,  d.path_features as path , d.area_of_district as area, ROUND(d.maximum_flood_water_extent,0) as under_water, ROUND(d.total_population_in_district,0) as papulation, ROUND(d.population_potentially_exposed,0) as exposed_papulation, ROUND(d.population_exposed,0) as exposed_papulation_percent FROM tabDistrict d INNER JOIN tabASC tac ON tac.district = d.name  LEFT JOIN  `tabFlood School` as tabimage   ON tac.semis_code = tabimage.semis_code   AND tac.year = tabimage.year  where tac.docstatus!=2 %s group by tac.district ORDER BY tac.region,tac.district ASC  """% (condition), as_dict=1)
        
    
    return data_


@frappe.whitelist()  
def get_images_data(basic_facility = None, year = None, division = None, district = None):
    condition= ''
    if district:
        condition += " and district= '%s' " % str(district) 

    data_ = frappe.db.sql("""SELECT   lat,  lng, area_name as name1, address, district, image from `tabFlood Images` where docstatus != 2  %s  """% (condition), as_dict=1)

    return data_