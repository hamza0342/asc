import frappe
@frappe.whitelist()
def get_data(district = None, division = None, taluka = None, level = None):
    condition = ""
    if division:
        condition += " and region= '%s' " % str(division)
    if district:
        condition += " and district= '%s' " % str(district)
    if taluka:
        condition += " and taluka= '%s' " % str(taluka)
    if level:
        condition += " and level= '%s' " % str(level)
  
    data_ = frappe.db.sql("""Select 
                            year, 
                            l.name as level, 
                            IFNULL(SUM(CASE WHEN school_gender = 'Boys'  THEN 1 Else 0 end),0) as boys, 
                            IFNULL(SUM(CASE WHEN school_gender = 'Girls' THEN 1 Else 0 end),0) as girls,
                            IFNULL(SUM(CASE WHEN school_gender = 'Mixed' THEN 1 Else 0 end),0) as mixed,
                            IFNULL(SUM(male_enrollment),0) as male,
                            IFNULL(SUM(female_enrollment),0) as female,
                            IFNULL(SUM(non_govt_female_teachers)+SUM(govt_female_teachers),0) as female_teachers,
                            IFNULL(SUM(non_govt_male_teachers)+SUM(govt_male_teachers),0) male_teachers
                            from `tabASC` a RIGHT JOIN `tabLevel` l ON level = l.name
                            where a.docstatus !=2   %s
                            group by year, l.name
                            order by year, l.list_order 
                        """%(condition), as_dict= 1)
    data = []
    data.append(data_) 
    if level:
         data.append(2) 
    else:
         data.append(6)      
    return data