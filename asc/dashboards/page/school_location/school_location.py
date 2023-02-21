import frappe
@frappe.whitelist()
def get_data(district = None, year = None, division = None, gender = None, level = None, status= None, semis_code= None, schools_having = None):
    default_year=frappe.db.get_single_value("ASC Panel", "default_year")
    condition = " and tac.year= '%s' " %default_year
    if division:
        condition += " and tac.region= '%s' " % str(division)
    if district:
        condition += " and tac.district= '%s' " % str(district)
    if gender:
        condition += " and tac.school_gender= '%s' " % str(gender)
    if level:
        condition += " and tac.level= '%s' " % str(level)
    if status:
        condition += " and tabimage.status= '%s' " % str(status)
    if semis_code:
        condition += " and tac.semis_code= '%s' " % str(semis_code)
    if schools_having:
        if schools_having == 'SEMIS Code':
            schools_having = 'Yes'
            condition += " and tabimage.semis_alloted= '%s' " % str(schools_having)
        if schools_having == 'Tracking ID':
            schools_having = 'No'
            condition += " and tabimage.semis_alloted= '%s' " % str(schools_having)
    #data_ = frappe.db.sql("""SELECT  `school_name` as School_name, `district`,`lat`,`lng`  FROM `tabASC Images` where `source`='Mobile' and docstatus!=2 %s"""% (condition), as_dict=1)
    
    # data_ = frappe.db.sql("""SELECT tabimage.semis_code, tabimage.`school_name` as School_name, tabimage.`district`,tabimage.`lat`,tabimage.`lng`, IFNULL(tac.level, "-") AS level, IFNULL(tac.school_gender,"-") AS school_gender  FROM `tabASC Images` as tabimage LEFT JOIN (SELECT school_gender,semis_code,level FROM tabASC group by semis_code) as tac ON tabimage.semis_code = tac.semis_code  where tabimage.`source`='Mobile' and tabimage.docstatus!=2 %s group by tabimage.semis_code """% (condition), as_dict=1)
    
    data_ = frappe.db.sql("""SELECT 
                            tac.name,
                            tabimage.semis_code, 
                            tabimage.`school_name` as School_name, 
                            tabimage.`district`,
                            tabimage.`gps_coordinateslatitude`,
                            tabimage.`gps_coordinateslongitude`, 
                            IFNULL(tac.level, "-") AS level, 
                            IFNULL(tac.school_gender,"-") AS school_gender,
                            tabimage.`status`
                            FROM `tabSchool` as tabimage 
                            INNER JOIN tabASC tac 
                            ON tabimage.name = tac.semis_code 
                            where tabimage.enabled = 1 %s 
                            group by tabimage.name 
                            """% (condition), as_dict=1)
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