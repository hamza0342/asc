# Copyright (c) 2021, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import utils
from frappe.model.document import Document

class ASC(Document):
	def validate(self):
		self.check_negative_values()
		self.validation_for_semis_code()
		self.check_child_tables()
		self.check_school_medium()
	def check_school_medium(self):
		if not self.sindhi_medium_enrolment:
			self.sindhi_medium_enrolment = 0
		if not self.urdu_medium_enrolment:
			self.urdu_medium_enrolment = 0
		if not self.english_medium_enrolment:
			self.english_medium_enrolment = 0
		sindhi, urdu, english = self.sindhi_medium_enrolment, self.urdu_medium_enrolment, self.english_medium_enrolment
		self.school_type = ""
		if sindhi > 0 and urdu == 0 and english == 0:
			self.school_type = 'Sindh'
		if sindhi == 0 and urdu > 0 and english == 0:
			self.school_type = 'Urdu'
		if sindhi == 0 and urdu == 0 and english > 0:
			self.school_type = 'English'
		if ((sindhi > 0 and urdu > 0) or (sindhi > 0 and english > 0) or (urdu > 0 and english > 0)):
			self.school_type = 'Mixed'			
			
	def check_child_tables(self):
		if len(self.gender_wise_enrolment) >= 1:
			final_tt = 0
			for xx in self.gender_wise_enrolment:
				frappe.msgprint(xx.boys)
				if self.school_gender == 'Girls':
					if not xx.girls:
						xx.girls = 0
					xx.boys = 0
					xx.total_class = xx.girls
					final_tt += xx.total_class
				
				if self.school_gender == 'Boys':
					if not xx.boys:
						xx.boys = 0
					xx.girls = 0
					xx.total_class = xx.boys
					final_tt += xx.total_class
				
				if self.school_gender == 'Mixed':
					if not xx.boys:
						xx.boys = 0
					if not xx.girls:
						xx.girls = 0
					xx.total_class = xx.boys + xx.girls
					final_tt += xx.total_class
				xx.overall_total = final_tt
			
		if len(self.table_repeaters) >= 1:
			final_tt = 0
			for xx in self.table_repeaters:
				frappe.msgprint(xx.boys)
				if self.school_gender == 'Girls':
					if not xx.girls:
						xx.girls = 0
					xx.boys = 0
					xx.total = xx.girls
					final_tt += xx.total
				
				if self.school_gender == 'Boys':
					if not xx.boys:
						xx.boys = 0
					xx.girls = 0
					xx.total = xx.boys
					final_tt += xx.total
				
				if self.school_gender == 'Mixed':
					if not xx.boys:
						xx.boys = 0
					if not xx.girls:
						xx.girls = 0
					xx.total = xx.boys + xx.girls
					final_tt += xx.total
				xx.overall = final_tt
		if not self.polio_affected:
			self.polio_affected = 0
		if not self.physical_disabilites:
			self.physical_disabilites = 0
		self.total_disables = self.polio_affected + self.physical_disabilites
		
	def validation_for_semis_code(self):
		if self.share_building_code:
			response = share_semis_code(self.share_building_code, self.district, self.semis_code)
			if response[0] == 1:
				self.share_building_code = ''
				self.shared_school_name = ''
				frappe.throw("District should be same for both schools")				
			else:
				self.shared_school_name = response[1]		

		if self.adjacent_schools:
			for x in self.adjacent_schools:
				if x.semis_code:
					response = share_semis_code(x.semis_code, self.district, self.semis_code)
					if response[0] == 1:
						self.semis_code = ''
						frappe.throw("District should be same for both schools")
					else:
						self.school_name_prefix_and_name = response[1]

		if self.semis:
			response = share_semis_code(self.semis, self.district, self.semis_code)
			if response[0] == 1:
				self.semis = ''
				frappe.throw("District should be same for both schools")
			else:
				self.name_of_main_school = response[1]
	def check_negative_values(self):
		if self.share_building_code and self.share_building_code < 0:
			frappe.throw("Number is negative at section 3 (c)")

		if self.rooms_used_as_class and self.rooms_used_as_class < 0:
			frappe.throw("Number is negative at section 3 (g)")
			
		if self.total_rooms and self.total_rooms < 0:
			frappe.throw("Number is negative at section 3 (h)")
		
		if self.ecce and self.ecce < 0:
			frappe.throw("Number is negative at Section 3 (ecce)")
		
		if self.primary and self.primary < 0:
			frappe.throw("Number is negative at Section 3 (primary)")
		
		if self.post_primary and self.post_primary < 0:
			frappe.throw("Number is negative at Section 3 (post_primary)")
		
		if self.total_no_of_functional_toilets and self.total_no_of_functional_toilets < 0:
			frappe.throw("Number is negative at Section 4 (total_no_of_functional_toilets)")
		
		if self.total_no_of_non_functional_toilet and self.total_no_of_non_functional_toilet < 0:
			frappe.throw("Number is negative at Section 4 (total_no_of_non_functional_toilet)")
		
		if self.polio_affected and self.polio_affected < 0:
			frappe.throw("Number is negative at Section 4 (polio_affected)")
		
		if self.physical_disabilites and self.physical_disabilites < 0:
			frappe.throw("Number is negative at Section 4 (physical_disabilites)")
		
		if self.semis and self.semis < 0:
			frappe.throw("Number is negative at Section 5 (b)")
		
		if self.no_of_merger_schools and self.no_of_merger_schools < 0:
			frappe.throw("Number is negative at Section 5 (no_of_merger_schools)")
		
		if self.no_of_sef_schools and self.no_of_sef_schools < 0:
			frappe.throw("Number is negative at Section 5 (no_of_sef_schools)")
		
		if self.no_of_private_schools and self.no_of_private_schools < 0:
			frappe.throw("Number is negative at Section 5 (no_of_private_schools)")

		if self.govt_male_teachers and self.govt_male_teachers < 0:
			frappe.throw("Number is negative at Section 10 (govt_male_teachers)")

		if self.govt_female_teachers and self.govt_female_teachers < 0:
			frappe.throw("Number is negative at Section 10 (govt_female_teachers)")
		
		if self.non_govt_male_teachers and self.non_govt_male_teachers < 0:
			frappe.throw("Number is negative at Section 10 (non_govt_male_teachers)")
		
		if self.non_teaching_male_staff and self.non_teaching_male_staff < 0:
			frappe.throw("Number is negative at Section 10 (non_teaching_male_staff)")

		if self.non_teaching_female_staff and self.non_teaching_female_staff < 0:
			frappe.throw("Number is negative at Section 10 (non_teaching_female_staff)")
		
		if self.non_govt_female_teachers and self.non_govt_female_teachers < 0:
			frappe.throw("Number is negative at Section 5 (non_govt_female_teachers)")
		
		if self.non_govt_female_teachers and self.non_govt_female_teachers < 0:
			frappe.throw("Number is negative at Section 5 (non_govt_female_teachers)")
		
@frappe.whitelist()
def share_semis_code(semis_code=None, district=None, main_semis=None):
	if district and semis_code and main_semis: 
		return_name = ""
		shared_semis_code = frappe.db.sql(""" select name,IFNULL(school_name, " ") from `tabSchool` where district = %s and name=%s and name!=%s """,(district, semis_code, main_semis))
		if shared_semis_code:
			return_name = shared_semis_code[0][1]
			return 0, return_name
		else:
			return 1, return_name
		
@frappe.whitelist()
def get_defaults():
	reference_date = frappe.db.get_single_value("ASC Panel", "reference_date")
	default_year = frappe.db.get_single_value("ASC Panel", "default_year")
	date_time = frappe.utils.now()
	return [reference_date, default_year, date_time]
	
@frappe.whitelist()
def select_values():
	school_administration = frappe.db.sql("""select name from `tabSchool administration` order by list_order""")
	school_gender = frappe.db.sql("""select name from `tabSchool Gender` order by list_order""")
	source_information_closure = frappe.db.sql("""select name from `tabSource of information of closure of School` order by list_order""")
	major_reason_closure = frappe.db.sql("""select name from `tabWrite major reason for closure` order by list_order""")
	yes_relevant_code = frappe.db.sql("""select name from `tabCase In Availability of Building` order by list_order""")
	type_of_building = frappe.db.sql("""select name from `tabType of building` order by list_order""")
	condition_of_building = frappe.db.sql("""select name from `tabCondition of Building` order by list_order""")
	provision_drinking_water = frappe.db.sql("""select name from `tabMode of provision of Drinking Water` order by list_order""")
	construction_work_planned_completed = frappe.db.sql("""select name from `tabconstruction work planned` order by list_order""")
	designation = frappe.db.sql("""select name from `tabDesignation` order by name""")

	ret = {
		'school_administration': school_administration,
		'school_gender': school_gender,
		'source_information_closure':source_information_closure,
		'major_reason_closure':major_reason_closure,
		'yes_relevant_code':yes_relevant_code,
		'type_of_building':type_of_building,
		'condition_of_building':condition_of_building,
		'provision_drinking_water':provision_drinking_water,
		'construction_work_planned_completed':construction_work_planned_completed,
		'principal_designation':designation,
		'designation_enumerator':designation,
		'designation_education_officer':designation
	}
	return ret
	
@frappe.whitelist()
def check_roster(semis_code=None):
	return_name = 0
	if not "System Manager" in frappe.get_roles(frappe.session.user):
		if ("Data Entry Operator" in frappe.get_roles(frappe.session.user)):
			shared_semis_code = frappe.db.sql(""" select sp.name from `tabSchool Permission` as sp, `tabASC Roster` as ar where sp.parent=ar.name and sp.school = %s and ar.user=%s """,(semis_code, frappe.session.user))
			if not shared_semis_code:
				return_name = 1
	return return_name
	
@frappe.whitelist()
def level_wise_enrollment():
	enrolment_ = frappe.db.sql("""select program_name from `tabProgram` order by order_no""" ,as_dict=1)
	repeaters_ = frappe.db.sql("""select program_name from `tabProgram` where class>=4 and class<=10  order by order_no""" ,as_dict=1)
	facility_ = frappe.db.sql("""select facility from `tabFacility` """ ,as_dict=1)
	item_ =frappe.db.sql("""select name1 from `tabItem`  """ ,as_dict=1)

	data={
		'enrolment':enrolment_,
		'repeaters':repeaters_,
		'facility':facility_,
		'item':item_,
	}
	return data
	
@frappe.whitelist()
def get_merged_schools(semis_code=None):
	enrolment_ = []
	if semis_code:
		enrolment_ = frappe.db.sql("""select semis_code, school_name from `tabMerged Schools in Campus` where parent=%s order by semis_code""" ,(semis_code),as_dict=1)
		
	data={
		'enrolment':enrolment_,
		'length_':len(enrolment_),
	}
	return data
	
@frappe.whitelist()
def get_user_detail():
	return frappe.db.sql("""select first_name, IFNULL(district, "") from `tabUser` where enabled=1 and name=%s """,(frappe.session.user))
	
