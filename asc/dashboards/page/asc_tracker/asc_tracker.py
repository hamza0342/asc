import frappe

@frappe.whitelist()
def page_query():
    default_settings = frappe.get_doc('ASC Panel')
    default_year = default_settings.default_year
    # default_year = "2020-21"

    total_schools = frappe.db.sql("""select count(name) from `tabSchool` where enabled=1 """)[0][0]
    school_level = frappe.db.sql(""" select 
                                lt.name,
                                sum(case when lt.name = a.level then 1 else 0 end) as total                                 
                                from `tabLevel` lt,`tabASC` a                                    
                                where a.docstatus != 2 and a.year = '{0}'
                                group by lt.name
                                """.format(default_year))
    total_enrol = frappe.db.sql("""select SUM(IFNULL(urdu_medium_enrolment,0) + IFNULL(english_medium_enrolment,0) + IFNULL(sindhi_medium_enrolment,0)) from `tabASC` where year=%s and docstatus!=2""", (default_year))[0][0]
    total_staff = frappe.db.sql("""select SUM(IFNULL(total_teacher,0) + IFNULL(total_non_teaching_non_government_staff,0) + IFNULL(total_non_teaching_staff,0)) from `tabASC` where year=%s and docstatus!=2""", (default_year))[0][0]
    total_images= frappe.db.sql("""select count(*) from `tabASC Images` where year=%s""", (default_year))[0][0]
    
    stack =frappe.db.sql("""select 
                    sum(case when (year='{0}' and water_available='No' and docstatus!=2) then 1 else 0 end) as schools_no_water,
                    sum(case when (year='{0}' and electricity_connection='No Electricity Connection' and docstatus!=2) then 1 else 0 end) as schools_no_electricity,
                    sum(case when (year='{0}' and total_teacher=1 and docstatus!=2) then 1 else 0 end) as schools_single_teacher,
                    sum(case when (year='{0}' and availability_of_building='No' and docstatus!=2) then 1 else 0 end) as schools_no_building,
                    sum(case when (year='{0}' and docstatus!=2) then 1 else 0 end) as entered_asc_schools,
                    sum(case when (year='{0}' and status_detail='Functional' and docstatus!=2) then 1 else 0 end) as func_asc_schools,
                    sum(case when (year='{0}' and status_detail='Closed' and docstatus!=2) then 1 else 0 end) as closed_asc_schools
                    from `tabASC` 
                    where year='{0}' and docstatus!=2
                    """.format(default_year), as_dict=1)[0]
    district_asc = frappe.db.sql(""" select 
                        d.name,
                        sum(case when (a.district = d.name) then 1 else 0 end) as asc_count
                        from `tabASC` a, `tabDistrict` d
                        where a.docstatus!=2 and a.year=%s
                        group by d.name
                        """, (default_year))
    school_asc = frappe.db.sql(""" select 
                        sum(case when (s.district = d.name) then 1 else 0 end) as asc_count
                        from `tabSchool` s, `tabDistrict` d
                        group by d.name
                        """)
    district_images = frappe.db.sql(""" select 
                        sum(case when (a.district = d.name) then 1 else 0 end) as asc_count
                        from `tabASC Images` a, `tabDistrict` d
                        where a.docstatus!=2 and a.year=%s
                        group by d.name
                        """, (default_year))  
    dict_name=[]
    per_dict=[]
    img_per=[]
    chart_data=[]

    count = 0
    for x in district_asc:
        dict_name.append(x[0])
        for s in school_asc[count: count+1]:
            if s[0] != 0:
                v = x[1]/s[0]*100
                per_dict.append(round(v))
                break
        count+=1

    count = 0   
    for im in district_images:    
        for s in school_asc[count: count+1]:
            if s[0] != 0:
                i = im[0]/s[0]*100
                img_per.append(round(i))
                break
        count+=1

    count = 0
    for d in per_dict:    
        for img in img_per[count: count+1]:
            for name in dict_name[count: count+1]:
                row = [ d, img, name ]
                chart_data.append(row)
                break
            break
        count+=1
    chart_data.sort(key=lambda x: x[0], reverse=True)
    
    asc_per=[]
    image_per=[]
    districts=[]
    for xx in chart_data:
        asc_per.append(xx[0])
        image_per.append(xx[1])
        districts.append(xx[2])
    obj={
        "total_schools":total_schools,
        "total_staff":total_staff,
        "total_enrol":total_enrol,
        "total_images":total_images,
        "school_level":school_level,
        "stack":stack,
        "district_images":image_per,
        "district_names":districts,
        "per_dict":asc_per,
        "chart_data":chart_data,
    }
    return obj

