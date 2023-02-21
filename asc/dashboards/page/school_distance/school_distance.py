import frappe
@frappe.whitelist()
def get_data(distance = 1, semisfrom = None, semisto = None, nearby = None, distancenearby = None):
   # round( 
              # ( 6373000 * acos( least(1.0,  
                # cos( radians(a.latn) ) 
                # * cos( radians(gps_coordinateslatitude) ) 
                # * cos( radians(gps_coordinateslongitude) - radians(a.lone) ) 
                # + sin( radians(a.latn) ) 
                # * sin( radians(gps_coordinateslatitude) 
              # ) ) ) 
            # ), 1) as distance
    
    if distance=='2':
        fromdata_ = frappe.db.sql("""
                SELECT status, level, address, district, gender, school_name, gps_coordinateslatitude as latn,gps_coordinateslongitude as lone, name FROM tabSchool WHERE `name` = '%s' 
                """%(nearby), as_dict=1)
                
        data_ = frappe.db.sql("""SELECT status, level, address, district, gender, school_name,tabSchool.name, a.lone,a.latn ,gps_coordinateslatitude as lats, gps_coordinateslongitude as lngs,round( 
              (111111.1 *
                DEGREES(ACOS(LEAST(1.0, COS(RADIANS(a.latn))
                     * COS(RADIANS(gps_coordinateslatitude))
                     * COS(RADIANS(a.lone) - RADIANS(gps_coordinateslongitude))
                     + SIN(RADIANS(a.latn))
                     * SIN(RADIANS(gps_coordinateslatitude)))))), 1) as distance from tabSchool
                INNER JOIN (
                SELECT gps_coordinateslatitude as latn,gps_coordinateslongitude as lone, name FROM tabSchool WHERE `name` = '%s' 
                ) as a ON 	tabSchool.name != a.name	
                 
               HAVING distance <= %s """%(nearby,distancenearby), as_dict=1)
    else:
        
        fromdata_ = frappe.db.sql("""
                SELECT status, level, address, district, gender, school_name, gps_coordinateslatitude as latn,gps_coordinateslongitude as lone, name FROM tabSchool WHERE `name` = '%s' 
                """%(semisfrom), as_dict=1)
        data_ = frappe.db.sql("""SELECT status, level, address, district, gender, school_name,tabSchool.name, a.lone,a.latn ,gps_coordinateslatitude as lats, gps_coordinateslongitude as lngs,round( 
              (111111.1 *
                DEGREES(ACOS(LEAST(1.0, COS(RADIANS(a.latn))
                     * COS(RADIANS(gps_coordinateslatitude))
                     * COS(RADIANS(a.lone) - RADIANS(gps_coordinateslongitude))
                     + SIN(RADIANS(a.latn))
                     * SIN(RADIANS(gps_coordinateslatitude)))))), 1) as distance from tabSchool
                INNER JOIN (
                SELECT gps_coordinateslatitude as latn,gps_coordinateslongitude as lone, name FROM tabSchool WHERE `name` = '%s' 
                ) as a ON 	tabSchool.name != a.name	
                 
                where tabSchool.`name` = '%s'  """%(semisfrom,semisto), as_dict=1)
     
    
    data =[]
    data.append(fromdata_) 
    data.append(data_) 
    return data