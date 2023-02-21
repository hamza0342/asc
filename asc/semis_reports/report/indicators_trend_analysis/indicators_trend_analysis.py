# Copyright (c) 2013, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    
    get_year = frappe.db.get_list('Year', pluck='name', order_by='name asc')
    colmn = get_columns(get_year,filters)
    columns = colmn[0]
    data = get_data(filters,colmn[1])
    return columns, data    
   
def get_columns(census_year,filters):
    columns=[]
    case_string=""
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
        case_string = " region, "
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
            case_string =" region, district,"

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
        case_string +=" region, district,taluka, "

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
            columns.append(
                {
                        "label": _("") + str(census) ,
                        "fieldtype": "Int",
                        "fieldname": str(census).lower() ,
                        "width": 140
                    }
            )
            if filters.get('indicators_list') == 'School':
                case_string += " SUM( CASE WHEN year = '%s' THEN 1 ELSE 0 END ), " %(str(census))
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

    return columns , case_string


def get_data(filters, case_string):
    conditions , group_by = get_condition(filters)
    temp_query = ""
    if filters.get('group_list') == 'Level': 
        temp_query = "SELECT  %s  COUNT(tac.name) FROM tabASC tac Cross join tabLevel on tac.level = tabLevel.name WHERE tac.docstatus != 2 %s %s" % (
        str(case_string), conditions, group_by)
    else:
        temp_query = "SELECT  %s  COUNT(name) FROM tabASC WHERE docstatus != 2 %s %s" % (
        str(case_string), conditions, group_by)
    # frappe.msgprint(frappe.as_json(temp_query))
    info = frappe.db.sql(temp_query, filters)
    # frappe.msgprint(frappe.as_json(info))

    return info

def get_condition(filters):
    group_by=""
    conditions = ""
    if filters.get('group_list') == 'Region' : 
        group_by +=  "GROUP BY  region Order By region"
    elif filters.get('group_list') == 'District': 
        group_by +=  "GROUP BY  region,  district Order By region,  district"
    elif filters.get('group_list') == 'Taluka' : 
        group_by +=  "GROUP BY  taluka Order By region,  district,taluka"
    elif filters.get('group_list') == 'UC' : 
        group_by +=  "GROUP BY  uc Order By uc"  
    elif filters.get('group_list') == 'Level' : 
        group_by +=  "GROUP BY  Level Order By tabLevel.list_order" 





    if filters.get("division"):
        conditions += " AND  region = %(division)s"
    if filters.get("location"):
        conditions += "  AND  location = %(location)s"
    if filters.get("status"):
        conditions += "  AND  status_detail = %(status)s"
    if filters.get("school_type"):
        conditions += "  AND  school_type = %(school_type)s"
    if filters.get("building_availability"):
        conditions += "  AND  availability_of_building = %(building_availability)s"
    if filters.get("condition_of_building"):
        conditions += "  AND  condition_of_building = %(condition_of_building)s"
    if filters.get("electricity_connection"):
        conditions += "  AND  electricity_connection = %(electricity_connection)s"
    if filters.get("water_available"):
        conditions += "  AND  water_available = %(water_available)s"
    if filters.get("district"):
        conditions += "  AND  district = %(district)s"
    if filters.get("level"):
        conditions += "  AND  level = %(level)s"
    if filters.get("school_gender"):
        conditions += "  AND  school_gender = %(school_gender)s"
    return conditions, group_by
