# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    get_year = frappe.db.get_list('Year', pluck='name', order_by='name asc')
    case_string=""
    pass_string=""
    attr_string=""
    cons = get_condition(filters,case_string,pass_string,attr_string)
    case_string = cons[2]
    pass_string = cons[3]
    attr_string = cons[4]
    # frappe.msgprint(frappe.as_json(case_string))111
    colmn = get_columns(get_year,filters,case_string,pass_string,attr_string)
    columns = colmn[0]
    # frappe.msgprint(frappe.as_json(case_string))
    # frappe.msgprint(frappe.as_json(colmn[1]))222
    data = get_data(filters,colmn[1], colmn[2],cons[0],cons[1])
    
    # frappe.msgprint(frappe.as_json(data))//333
    return columns, data
def get_columns(census_year,filters,case_string,pass_string,attr_string):
    columns=[]
    case_string2=""
    district ="''"
    level=""
    sc_status=""
    gender=""
    e_connection=""
    s_water=""
    condition_buil=""
    loc=""
    b_availble=""
    if filters.get("level"):
        level=filters.get("level")
    if filters.get("status"):
        sc_status=filters.get("status")
    if filters.get("school_gender"):
        gender=filters.get("school_gender")
    if filters.get("electricity_connection"):
        e_connection=filters.get("electricity_connection")
    if filters.get("water_available"):
        s_water=filters.get("water_available")
    if filters.get("condition_of_building"):
        condition_buil=filters.get("condition_of_building")
    if filters.get("location"):
        loc=filters.get("location")
    if filters.get("building_availability"):
        b_availble=filters.get("building_availability")


    # frappe.msgprint(frappe.as_json(level))
    # frappe.msgprint(frappe.as_json(sc_status))
    # frappe.msgprint(frappe.as_json(e_connection))

    if filters.get('group_list') == 'Region' or filters.get('group_list') == 'District': 
        columns.append(
            {
                "label": _("Division"),
                "fieldtype": "Link",
                "fieldname": "division",
                 "options": "Division",
                "width": 170
            }
        )
        case_string += " Division, "
        case_string2 = " Division, "
        pass_string += " region=''',Division,''' "
        # pass_list.append("Division")


        # pass_string += Division
        attr_string +=""" ,this.getAttribute("region") """

        if not filters.get('group_list') == 'Region':
            columns.append(
                {
                    "label": _("District"),
                    "fieldtype": "Data",
                    "fieldname": "district",
                    "options": "District",
                    "width": 170
                }
            )
            case_string +="  District,"
            case_string2 +="  District,"
            pass_string += "  district=''',District,''' "
            # pass_list.append("District")
            attr_string +=""" ,this.getAttribute("district") """
            district ="District"



    if filters.get('group_list') == 'Taluka' : 
        columns.append(
            {
                "label": _("Division"),
                "fieldtype": "Link",
                "fieldname": "division",
                 "options": "Division",
                "width": 170
            }
        )
        columns.append(
                {
                    "label": _("District"),
                    "fieldtype": "Data",
                    "fieldname": "district",
                    "options": "District",
                    "width": 170
                }
            )
        columns.append(
            {
                "label": _("Taluka"),
                "fieldtype": "Data",
                "fieldname": "taluka",
                "width": 170
            }
        )
        case_string +=" Tehsil, "
        case_string2 =" Tehsil, "
        pass_string += " region=''',Division,''' district=''',District,''' taluka=''',Tehsil,'''"
        #  pass_list.append("Tehsil")
        attr_string +=""" ,this.getAttribute("region"),this.getAttribute("district"),this.getAttribute("taluka") """

    if filters.get('group_list') == 'UC' : 
        columns.append(
            {
                "label": _("Division"),
                "fieldtype": "Link",
                "fieldname": "division",
                 "options": "Division",
                "width": 170
            }
        )
        columns.append(
                {
                    "label": _("District"),
                    "fieldtype": "Data",
                    "fieldname": "district",
                    "options": "District",
                    "width": 170
                }
            )
        columns.append(
            {
                "label": _("Taluka"),
                "fieldtype": "Data",
                "fieldname": "taluka",
                "width": 170
            }
        )
        columns.append(
            {
                "label": _("Union Council"),
                "fieldtype": "Data",
                "fieldname": "uc",
                "width": 220
            }
        )
        case_string +=" region, district,taluka,  uc, "


    if filters.get('group_list') == 'Level': 
        columns.append(
            {
                "label": _("Level"),
                "fieldtype": "Data",
                "fieldname": "level",
                "width": 170
            }
        )
        case_string = " level, "

    if filters.get('columns_list') == 'Year wise Analysis':
        for census in census_year:
            # frappe.msgprint(frappe.as_json(census))
            columns.append(
                {
                        "label": _("") + str(census) ,
                        "fieldtype": "Data",
                        "fieldname": str(census).lower() ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':

                # frappe.msgprint(frappe.as_json(case_string))
                # frappe.msgprint(frappe.as_json(str(census)))
                frappe.msgprint(frappe.as_json(pass_string))

                case_string += " SUM( CASE WHEN Year = '%s' THEN 1 ELSE 0 END ) as '%s', " %(str(census),str(census))

                case_string2 += """ CONCAT('<a Test=''', `%s` ,''' Division=''', Division ,'''  district =''', %s ,''' Year=''','%s',''' levels=''','%s',''' s_status=''','%s',''' s_gender=''','%s',''' ele_con=''','%s',''' water=''','%s',''' buil_cond=''','%s',''' s_loc=''','%s',''' b_avail=''','%s','''%s type=''button''  onClick=''open_report(this.getAttribute("Test"), this.getAttribute("Year") ,this.getAttribute("levels") ,this.getAttribute("s_status"),this.getAttribute("s_gender"),this.getAttribute("ele_con"),this.getAttribute("water"),this.getAttribute("buil_cond"),this.getAttribute("s_loc"),this.getAttribute("b_avail"),this.getAttribute("Division"),this.getAttribute("district")%s)''>',`%s`,'</a>') as ":Data:100", """%(str(census),district,str(census),level,sc_status,gender,e_connection,s_water,condition_buil,loc,b_availble,pass_string,attr_string,str(census))
                # case_string += """<a>SUM( CASE WHEN year = '2021-22' THEN 1 ELSE 0 END ) </a> as abc ,"""
                frappe.msgprint(frappe.as_json(case_string2))
            elif filters.get('indicators_list') == 'Total Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' THEN (english_medium_enrolment + urdu_medium_enrolment + sindhi_medium_enrolment) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Male Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' THEN male_enrollment ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Female Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' THEN female_enrollment ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Male Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (IFNULL(govt_male_teachers,0)  + IFNULL(non_govt_male_teachers,0)  + IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0))  ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Female Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN ( IFNULL(govt_female_teachers,0)  +IFNULL(non_govt_female_teachers,0)  + IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Total Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (IFNULL(govt_male_teachers,0) + IFNULL(govt_female_teachers,0) + IFNULL(non_govt_male_teachers,0) +IFNULL(non_govt_female_teachers,0) + IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Male Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (govt_male_teachers  + non_govt_male_teachers ) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Female Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN ( govt_female_teachers  + non_govt_female_teachers) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Total Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Male Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0)) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Female Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN ( IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census))
            elif filters.get('indicators_list') == 'Total Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' THEN (IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census))
    
    
    elif filters.get('columns_list') == 'School Level':
        level_list = ["Primary", "Middle", "Elementary", "Secondary", "Higher Secondary"]
        census = filters.get('year')
        for level in level_list:
            columns.append(
                {
                        "label": _("") + str(level) ,
                        "fieldtype": "Int",
                        "fieldname": str(level).lower().replace(" ","_") ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN 1 ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Total Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (english_medium_enrolment + urdu_medium_enrolment + sindhi_medium_enrolment) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Male Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN male_enrollment ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Female Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN female_enrollment ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Male Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (IFNULL(govt_male_teachers,0)  + IFNULL(non_govt_male_teachers,0)  + IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0))  ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Female Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN ( IFNULL(govt_female_teachers,0)  +IFNULL(non_govt_female_teachers,0)  + IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Total Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (IFNULL(govt_male_teachers,0) + IFNULL(govt_female_teachers,0) + IFNULL(non_govt_male_teachers,0) +IFNULL(non_govt_female_teachers,0) + IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Male Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (govt_male_teachers  + non_govt_male_teachers ) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Female Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN ( govt_female_teachers  + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Total Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Male Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0)) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Female Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN ( IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(level))
            elif filters.get('indicators_list') == 'Total Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and level = '%s' THEN (IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(level))
    
    elif filters.get('columns_list') == 'School Gender':
        gender_list = ["Boys", "Girls", "Mixed"]
        census = filters.get('year')
        for gender in gender_list:
            columns.append(
                {
                        "label": _("") + str(gender) ,
                        "fieldtype": "Int",
                        "fieldname": str(gender).lower().replace(" ","_") ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN 1 ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Total Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (english_medium_enrolment + urdu_medium_enrolment + sindhi_medium_enrolment) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Male Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN male_enrollment ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Female Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN female_enrollment ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Male Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (IFNULL(govt_male_teachers,0)  + IFNULL(non_govt_male_teachers,0)  + IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0))  ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Female Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN ( IFNULL(govt_female_teachers,0)  +IFNULL(non_govt_female_teachers,0)  + IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Total Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (IFNULL(govt_male_teachers,0) + IFNULL(govt_female_teachers,0) + IFNULL(non_govt_male_teachers,0) +IFNULL(non_govt_female_teachers,0) + IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Male Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (govt_male_teachers  + non_govt_male_teachers ) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Female Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN ( govt_female_teachers  + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Total Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Male Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0)) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Female Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN ( IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(gender))
            elif filters.get('indicators_list') == 'Total Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_gender = '%s' THEN (IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(gender))
   
    elif filters.get('columns_list') == 'School Type':
        medium_list = ["Sindhi", "Urdu", "English", "Mixed"]
        census = filters.get('year')
        for medium in medium_list:
            columns.append(
                {
                        "label": _("") + str(medium) ,
                        "fieldtype": "Int",
                        "fieldname": str(medium).lower().replace(" ","_") ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN 1 ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Total Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (english_medium_enrolment + urdu_medium_enrolment + sindhi_medium_enrolment) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Male Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN male_enrollment ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Female Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN female_enrollment ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Male Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (IFNULL(govt_male_teachers,0)  + IFNULL(non_govt_male_teachers,0)  + IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0))  ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Female Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN ( IFNULL(govt_female_teachers,0)  +IFNULL(non_govt_female_teachers,0)  + IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Total Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (IFNULL(govt_male_teachers,0) + IFNULL(govt_female_teachers,0) + IFNULL(non_govt_male_teachers,0) +IFNULL(non_govt_female_teachers,0) + IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Male Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (govt_male_teachers  + non_govt_male_teachers ) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Female Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN ( govt_female_teachers  + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Total Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Male Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0)) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Female Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN ( IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(medium))
            elif filters.get('indicators_list') == 'Total Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and school_type = '%s' THEN (IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(medium))
    elif filters.get('columns_list') == 'School Status':
        status_list = ["Functional", "Closed"]
        census = filters.get('year')
        for status in status_list:
            columns.append(
                {
                        "label": _("") + str(status) ,
                        "fieldtype": "Int",
                        "fieldname": str(status).lower().replace(" ","_") ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN 1 ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Total Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (english_medium_enrolment + urdu_medium_enrolment + sindhi_medium_enrolment) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Male Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN male_enrollment ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Female Enrollment':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN female_enrollment ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Male Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (IFNULL(govt_male_teachers,0)  + IFNULL(non_govt_male_teachers,0)  + IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0))  ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Female Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN ( IFNULL(govt_female_teachers,0)  +IFNULL(non_govt_female_teachers,0)  + IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Total Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (IFNULL(govt_male_teachers,0) + IFNULL(govt_female_teachers,0) + IFNULL(non_govt_male_teachers,0) +IFNULL(non_govt_female_teachers,0) + IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Male Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (govt_male_teachers  + non_govt_male_teachers ) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Female Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN ( govt_female_teachers  + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Total Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (govt_male_teachers + govt_female_teachers + non_govt_male_teachers + non_govt_female_teachers) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Male Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (IfNULL(non_teaching_male_staff,0)  + IfNULL(non_teaching_non_government_male_staff,0)) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Female Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN ( IfNULL(non_teaching_female_staff,0)  + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(status))
            elif filters.get('indicators_list') == 'Total Non-Teaching Staff':
                case_string += " SUM( CASE WHEN year = '%s' and status_detail = '%s' THEN (IfNULL(non_teaching_male_staff,0) + IfNULL(non_teaching_female_staff,0) + IfNULL(non_teaching_non_government_male_staff,0) + IfNULL(non_teaching_non_government_female_staff,0)) ELSE 0 END ), " %(str(census),str(status))

    return columns , case_string , case_string2


def get_data(filters, case_string , case_string2,conditions , group_by):
    temp_query = ""
    if filters.get('group_list') == 'Level': 
        temp_query = "SELECT  %s  COUNT(tac.name) FROM tabASC tac Cross join tabLevel on tac.level = tabLevel.name WHERE tac.docstatus != 2 %s %s" % (
        str(case_string), conditions, group_by)
    else:
        frappe.db.sql("DROP VIEW IF EXISTS tempo;")
        temp_query = "Create View tempo as SELECT  %s  COUNT(id) as a  from tabASC_KPI WHERE 1 %s %s" % (
        str(case_string), conditions, group_by)
        frappe.msgprint(frappe.as_json(temp_query))
        info = frappe.db.sql(temp_query)
        temp_query = """SELECT  %s  a as a  FROM tempo """ %(case_string2)
    frappe.msgprint(frappe.as_json(temp_query))
    info = frappe.db.sql(temp_query)
    frappe.db.sql("DROP VIEW tempo")
    # frappe.msgprint(frappe.as_json(info))

    return info

def get_condition(filters,case_string,pass_string,attr_string):
    group_by=""
    conditions = ""
    if filters.get('group_list') == 'Region' : 
        group_by +=  "GROUP BY  Division Order By Division"
    elif filters.get('group_list') == 'District': 
        group_by +=  "GROUP BY  Division,  District Order By Division,  District"
    elif filters.get('group_list') == 'Taluka' : 
        group_by +=  "GROUP BY  Tehsil Order By Division,  District,Tehsil"
    elif filters.get('group_list') == 'UC' : 
        group_by +=  "GROUP BY  uc Order By uc"  
    elif filters.get('group_list') == 'Level' : 
        group_by +=  "GROUP BY  Level Order By tabLevel.list_order" 





    if filters.get("division"):
        s_division=filters.get("division")
        conditions += " AND  Division = '%s' "%(s_division)
        case_string +=" Division, "
        pass_string += " region=''',Division,''' "
        attr_string +=""" ,this.getAttribute("region") """
    if filters.get("location"):
        s_location=filters.get("location")
        conditions += "  AND  Location = '%s' "%(s_location)
        case_string +=" Location, "
        pass_string += " location=''',Location,''' "
        attr_string +=""" ,this.getAttribute("location") """
    if filters.get("status"):
        s_status=filters.get("status")
        conditions += "  AND  Status = '%s' "%(s_status)
        case_string +=" Status, "
        pass_string += " status=''',Status,''' "
        attr_string +=""" ,this.getAttribute("status") """
    if filters.get("school_type"):
        conditions += "  AND  school_type = %(school_type)s"
    if filters.get("building_availability"):
        a_building=filters.get("building_availability")
        conditions += "  AND  `Building Availability` = '%s' "%(a_building)
        case_string +=" `Building Availability`, "
        pass_string += " availbilty=''',`Building Availability`,''' "
        attr_string +=""" ,this.getAttribute("availbilty") """
    if filters.get("condition_of_building"):
        c_building=filters.get("condition_of_building")
        conditions += "  AND  `Building Condition` = '%s' "%(c_building)
        case_string +=" `Building Condition`, "
        pass_string += " b_condition=''',`Building Condition`,''' "
        attr_string +=""" ,this.getAttribute("b_condition") """
    if filters.get("electricity_connection"):
        s_electricity=filters.get("electricity_connection")
        conditions += "  AND  Electricity = '%s' "%(s_electricity)
        case_string +=" Electricity, "
        pass_string += " e_condition=''',Electricity,''' "
        attr_string +=""" ,this.getAttribute("e_condition") """ 
    if filters.get("water_available"):
        s_water=filters.get("water_available")
        conditions += "  AND  Water = '%s' "%(s_water)
        case_string +=" Water, "
        pass_string += " water=''',Water,''' "
        attr_string +=""" ,this.getAttribute("water") """
    if filters.get("district"):
        s_district=filters.get("district")
        conditions += "  AND  District = '%s' "%(s_district)
        case_string +=" District, "
        pass_string += " district=''',District,''' "
        attr_string +=""" ,this.getAttribute("district") """
        
    if filters.get("level"):
        s_level=filters.get("level")
        conditions += "  AND  Level = '%s' "%(s_level)
        case_string +=" Level, "
        # pass_string += Level
        pass_string += " level=''',Level,''' "
        # pass_list.append
        attr_string +=""" ,this.getAttribute("level") """
    if filters.get("school_gender"):
        # frappe.msgprint(frappe.as_json(filters.get("school_gender")))
        gender=filters.get("school_gender")
        # frappe.msgprint(frappe.as_json(gender))
        conditions += "  AND  Gender = '%s' "%(gender)
        case_string +=" Gender, "
        pass_string += " gender=''',Gender,''' "
        attr_string +=""" ,this.getAttribute("gender") """
    return conditions, group_by ,case_string,pass_string,attr_string
