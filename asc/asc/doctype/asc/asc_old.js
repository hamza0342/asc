// // Copyright (c) 2021, Frappe Technologies and contributors
// // For license information, please see license.txt
frappe.require([
	'/assets/semis_theme/js/personal_detail_validation.js',
]);
const asc_fields = ["semis_code", "visit_date_and_time", "location", "uc", "ena_constituency", "fps_constituency", "present_address", "ddo_cost_center", "school_gender", "shift", "school_phone_no", "school_administration"
	, "status_detail", "school_duration_of_closure", "source_information_closure", "major_reason_closure", "closure_any_other_reasons_text", "availability_of_building", "yes_relevant_code", "share_building_code", "type_of_building", "condition_of_building", "no_relevant_other", "no_relevant_code"
	, "yes_relevant_other", "total_area_school", "total_rooms_school", "ecce", "primary", "post_primary", "water_available", "source_drinking_water", "provision_drinking_water", "electricity_connection", "no_connection_reason", "status_of_electrification", "condition_of_boundary_wall", "toilet_facility", "total_no_of_functional_toilets"
	, "total_no_of_non_functional_toilet", "non_functional_toilet_reasons", "toilets_accessible_disabled", "wheel_chair_ramp_available", "polio_affected", "physical_disabilites", "hand_wash_facility", "mhm_facility", "disposal_for_sanitary"
	, "tree_plantation_school", "branch_school_and_adoption_of_school_information_section", "adopted_school", "is_this_branch_school", "semis", "adopter_name", "is_campus_school", "adjacent_schools", "no_of_sef_schools", "no_of_private_schools", "details_repair_in_school__year", "construction_work_planned_completed"
	, "what_constructed_in_school", "what_constructed_text", "status_of_facilities_availability", "status_items_availability", "smc_received_detail", "t_r_smc", "utlized", "m_repair", "cleanliness", "trans_for_g_c", "school_registers", "sindhi_medium_enrolment", "urdu_medium_enrolment", "english_medium_enrolment", "gender_wise_enrolment", "table_repeaters", "govt_male_teachers"
	, "govt_female_teachers", "non_govt_male_teachers", "non_govt_female_teachers", "non_teaching_male_staff", "non_teaching_female_staff"
	, "principal_hm_name", "principal_email", "principal_designation", "cnic_number_principal", "principal_phone", "principal_gender",
	"date_principal", "name_enumerator", "cnic_no_enumerator", "designation_enumerator", "contact_no_enumerator", "staff_detail",
	"completion_check", "lat_n", "lon_e"]

frappe.ui.form.on('ASC', {
	semis_code: function (frm) {
		if (frm.doc.semis_code) {
			frappe.call({
				method: "asc.asc.doctype.asc.asc.check_roster",
				args: {
					semis_code: frm.doc.semis_code
				},
				callback: function (r) {
					if (r.message == 1) {
						frm.set_value("semis_code", '');
						frm.set_value("lat_n", '');
						frm.set_value("lon_e", '');
						frm.set_value("region", '');
						frm.set_value("district", '');
						frm.set_value("taluka", '');
						frm.set_value("uc", '');
						frm.set_value("school_name", '');
						frm.set_value("present_address", '');
						frm.set_value("location", '');
						frm.set_value("level", '');
						frm.set_value("school_gender", '');
						frm.set_value("shift", '');
						frm.set_value("school_phone_no", '');
						frm.set_value("school_administration", '');
						frappe.msgprint("School Not Assigned")
					}
				}
			});
		}
	},
	region: function (frm) {
		if (!frm.doc.region) {
			frm.set_value("district", '');
			frm.set_value("taluka", '')
		}
	},
	district: function (frm) {
		if (!frm.doc.district) {
			frm.set_value("taluka", '')
		}
	},
	taluka: function (frm) {
		if (!frm.doc.taluka) {
			frm.set_value("uc", '')
		}
	},
	ena_constituency: function (frm) {
		if (!Number.isInteger(frm.doc.ena_constituency)) {
			frm.set_value("ena_constituency", '')
		}
		if (frm.doc.ena_constituency < 0) {
			frm.set_value("ena_constituency", '')
			frappe.msgprint("Must be a valid Number..")
		}
	},
	fps_constituency: function (frm) {
		if (!Number.isInteger(frm.doc.fps_constituency)) {
			frm.set_value("fps_constituency", '')
		}
		if (frm.doc.fps_constituency < 0) {
			frm.set_value("fps_constituency", '')
			frappe.msgprint("Must be a valid Number..")
		}
	},

	/*school_phone_no:function(frm){
		if (frm.doc.school_phone_no){
			$("input[data-fieldname='school_phone_no']").focusout(function () {
				var num = frm.doc.school_phone_no
				if (!(phone_validate(num))) {
					$(".msgprint").empty()
					frappe.msgprint("Please Enter valid phone number")
					frm.set_value("school_phone_no", '')
				}
			});
		}
		
		},*/
	smc_received_detail: function (frm) {
		if (frm.doc.smc_received_detail) {
			frm.set_value("t_r_smc", '');
			frm.set_value("utlized", '');
			frm.set_value("m_repair", '');
			frm.set_value("cleanliness", '');
			frm.set_value("trans_for_g_c", '');
		}
	},
	school_gender: function (frm) {
		if (frm.doc.school_gender == "Mixed") {
			frm.set_value("school_administration", 'Taluka Education Officer (Male)')
		}

		if (frm.doc.school_gender == "Boys") {

			frm.set_query("school_administration", function () {
				frm.set_value("school_administration", '')
				return {
					"filters": [
						["School administration", "name1", "in", ['Taluka Education Officer (Male)', 'TEO Male', 'DO Local Bodies', 'Bureau of Curriculum']]

					]
				};
			});
		}

		if (frm.doc.school_gender == "Girls") {
			frm.set_value("school_administration", '')
			frm.set_query("school_administration", function () {
				return {
					"filters": [
						["School administration", "name1", "in", ['Taluka Education Officer (Female)', 'TEO Female', 'DO Local Bodies', 'Bureau of Curriculum']]

					]
				};
			});
		}
	},
	status_detail: function (frm) {
		if (frm.doc.status_detail) {
			frm.set_value("source_information_closure", '');
			frm.set_value("school_duration_of_closure", '');
			frm.set_value("major_reason_closure", '');
		}
		if (frm.doc.status_detail == "Closed") {
			frm.set_df_property("source_information_closure", "reqd", 1);
			frm.set_df_property("school_duration_of_closure", "reqd", 1);
			frm.set_df_property("major_reason_closure", "reqd", 1);
			cur_frm.clear_table("gender_wise_enrolment");
			cur_frm.clear_table("table_repeaters");
			cur_frm.clear_table("status_of_facilities_availability");
			cur_frm.clear_table("status_items_availability");
		}
		if (frm.doc.status_detail == "Functional") {
			frm.set_df_property("source_information_closure", "reqd", 0);
			frm.set_df_property("school_duration_of_closure", "reqd", 0);
			frm.set_df_property("major_reason_closure", "reqd", 0);

			cur_frm.clear_table("gender_wise_enrolment");
			cur_frm.clear_table("table_repeaters");
			cur_frm.clear_table("status_of_facilities_availability");
			cur_frm.clear_table("status_items_availability");
			frappe.call({
				method: "asc.asc.doctype.asc.asc.level_wise_enrollment",
				callback: function (response) {
					var enrolment = response.message.enrolment;
					var repeaters = response.message.repeaters;
					var facility = response.message.facility;
					var item = response.message.item;

					for (let i = 0; i < enrolment.length; i++) {
						var row = frappe.model.add_child(cur_frm.doc, "ASC", "gender_wise_enrolment");
						row.class = enrolment[i].program_name;
						refresh_field("gender_wise_enrolment");

					}
					for (let i = 0; i < repeaters.length; i++) {
						var row = frappe.model.add_child(cur_frm.doc, "ASC", "table_repeaters");
						row.class = repeaters[i].program_name;
						refresh_field("table_repeaters");
					}
					for (let i = 0; i < facility.length; i++) {
						var row = frappe.model.add_child(cur_frm.doc, "ASC", "status_of_facilities_availability");
						row.facility = facility[i].facility;
						row.status = "Not Available";
						refresh_field("status_of_facilities_availability");
					}
					for (let i = 0; i < item.length; i++) {
						var row = frappe.model.add_child(cur_frm.doc, "ASC", "status_items_availability");
						row.items = item[i].name1;
						refresh_field("status_items_availability");
					}
				}
			})
		}
	},
	availability_of_building: function (frm) {
		if (frm.doc.availability_of_building) {
			frm.set_value("yes_relevant_code", '');
			frm.set_value("type_of_building", '');
			frm.set_value("condition_of_building", '');
			frm.set_value("total_area_school", '');
			frm.set_value("total_rooms_school", '');
			//frm.set_value("rooms_used_as_class",'');
			frm.set_value("share_building_code", '');
			frm.set_value("no_relevant_other", '');
			frm.set_value("no_relevant_code", '');
			frm.set_value("yes_relevant_other", '');
			frm.set_value("ecce", '');
			frm.set_value("primary", '');
			frm.set_value("post_primary", '');
			frm.set_value("post_primary", '');


		}
		if (frm.doc.availability_of_building == "Yes") {
			frm.set_df_property("yes_relevant_code", "reqd", 1);
			frm.set_df_property("type_of_building", "reqd", 1);
			frm.set_df_property("condition_of_building", "reqd", 1);
			frm.set_df_property("total_area_school", "reqd", 1);
			frm.set_df_property("total_rooms_school", "reqd", 1);
			//frm.set_df_property("rooms_used_as_class", "reqd", 1);
		}
		else {
			frm.set_df_property("yes_relevant_code", "reqd", 0);
			frm.set_df_property("type_of_building", "reqd", 0);
			frm.set_df_property("condition_of_building", "reqd", 0);
			frm.set_df_property("total_area_school", "reqd", 0);
			frm.set_df_property("total_rooms_school", "reqd", 0);
			//frm.set_df_property("rooms_used_as_class", "reqd", 0);
		}
	},
	school_duration_of_closure: function (frm) {
		if (frm.doc.school_duration_of_closure == 'Less than 1 year') {
			frm.set_value("closed_type", 'Closed Temporary');
		}
		else if (frm.doc.school_duration_of_closure == 'Less than 2 years') {
			frm.set_value("closed_type", 'Closed Permanent');
		}
		else if (frm.doc.school_duration_of_closure == 'Less than 3 years') {
			frm.set_value("closed_type", 'Viable Closed');
		}
		else if (frm.doc.school_duration_of_closure == '4 years or More') {
			frm.set_value("closed_type", 'Non-Viable');
		}
		else {
			frm.set_value("closed_type", '');
		}
	},
	/*construction_work_planned_completed:function(frm){
		if (frm.doc.what_constructed_in_school=='No work done' && frm.doc.construction_work_planned_completed=='Yes') {
			frappe.msgprint(`'Yes' can't be selected if 'No work done' selected for 'Please mention what was constructed in School'`)
			frm.set_value("construction_work_planned_completed",'');
		}
	},
	what_constructed_in_school:function(frm){
		if (frm.doc.construction_work_planned_completed=='Yes' && frm.doc.what_constructed_in_school=='No work done') {
			frappe.msgprint(`'No work done' can't be selected if 'Yes' selected for 'If any construction work planned, then has the work completed?'`)
			frm.set_value("what_constructed_in_school",'');
		}
	},*/

	semis: function (frm) {
		if (frm.doc.semis && frm.doc.district) {
			frappe.call({
				method: "asc.asc.doctype.asc.asc.share_semis_code",
				args: {
					semis_code: frm.doc.semis,
					district: frm.doc.district,
					main_semis: frm.doc.semis_code
				},
				callback: function (r) {
					if (r.message[0] == 1) {
						//frm.set_value("semis",'');
						frm.set_value("name_of_main_school", '');
						frappe.msgprint("District should be same for both schools")
					}
					else {
						frm.set_value("name_of_main_school", r.message[1]);
					}
				}
			});
		}

	},
	share_building_code: function (frm) {
		if (!Number.isInteger(frm.doc.share_building_code)) {
			frm.set_value("share_building_code", '')
		}
		if (frm.doc.share_building_code < 0) {
			frm.set_value("share_building_code", '')
			frappe.msgprint("Must be a valid SEMIS Code.")
		}
		if (frm.doc.share_building_code && frm.doc.district) {
			frappe.call({
				method: "asc.asc.doctype.asc.asc.share_semis_code",
				args: {
					semis_code: frm.doc.share_building_code,
					district: frm.doc.district,
					main_semis: frm.doc.semis_code
				},
				callback: function (r) {
					if (r.message[0] == 1) {
						frm.set_value("share_building_code", '');
						frm.set_value("shared_school_name", '');
						frappe.msgprint("District should be same for both schools")
					}
					else {
						frm.set_value("shared_school_name", r.message[1]);
					}
				}
			});
		}
	},
	total_area_school: function (frm) {
		if (!Number.isInteger(frm.doc.total_area_school)) {
			frm.set_value("total_area_school", '')
		}
		if (frm.doc.total_area_school < 0) {
			frm.set_value("total_area_school", '')
			frappe.msgprint("Must be a valid Number.")
		}
	},
	total_rooms_school: function (frm) {
		if (!Number.isInteger(frm.doc.total_rooms_school)) {
			frm.set_value("total_rooms_school", '')
		}
		if (frm.doc.total_rooms_school < 0) {
			frm.set_value("total_rooms_school", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (frm.doc.total_rooms_school && frm.doc.total_rooms && frm.doc.total_rooms_school < frm.doc.total_rooms) {
			frm.set_value("total_rooms", '');
			frm.set_value("ecce", '');
			frm.set_value("primary", '');
			frm.set_value("post_primary", '')
			frappe.msgprint("Used classroom should be less or equal to the total rooms in the school")
		}
		if (frm.doc.total_rooms_school && frm.doc.total_no_of_functional_toilets && frm.doc.total_rooms_school < frm.doc.total_no_of_functional_toilets) {
			frm.set_value("total_no_of_functional_toilets", '')
			frappe.msgprint("Total No Of Functional Toilets should be less or equal to the Total number of rooms in School")
		}
	},
	/*rooms_used_as_class:function(frm){
		if (!Number.isInteger(frm.doc.rooms_used_as_class)){
			frm.set_value("rooms_used_as_class",'')
		}
		if(frm.doc.rooms_used_as_class < 0){
			frm.set_value("rooms_used_as_class",'')
			frappe.msgprint("Must be a valid Number.")
		}
		frm.set_value("total_rooms",'');
		frm.set_value("ecce",'');
		frm.set_value("primary",'');
			  frm.set_value("post_primary", '')

	   if (frm.doc.total_rooms_school <= frm.doc.rooms_used_as_class - 1) {
			   frm.set_value("rooms_used_as_class",'');
				 frappe.msgprint("Enter Total Rooms First and Used Classrooms must be less or equal to the Total Rooms.")
	   }
	   
	},*/
	ecce: function (frm) {
		if (!Number.isInteger(frm.doc.ecce)) {
			frm.set_value("ecce", '')
		}
		if (frm.doc.ecce < 0) {
			frm.set_value("ecce", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.ecce) {
			frm.doc.ecce = 0;
		}
		if (!frm.doc.primary) {
			frm.doc.primary = 0;
		}
		if (!frm.doc.post_primary) {
			frm.doc.post_primary = 0;
		}
		var total = frm.doc.ecce + frm.doc.primary + frm.doc.post_primary;
		frm.set_value("total_rooms", total);
		if (total > frm.doc.total_rooms_school) {
			frappe.msgprint("Used classroom should be less or equal to the total rooms in the school")
			frm.set_value("total_rooms", '');
			frm.set_value("ecce", '');
			frm.set_value("primary", '');
			frm.set_value("post_primary", '')
		}
	},
	primary: function (frm) {
		if (!Number.isInteger(frm.doc.primary)) {
			frm.set_value("primary", '')
		}
		if (frm.doc.primary < 0) {
			frm.set_value("primary", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.ecce) {
			frm.doc.ecce = 0;
		}
		if (!frm.doc.primary) {
			frm.doc.primary = 0;
		}
		if (!frm.doc.post_primary) {
			frm.doc.post_primary = 0;
		}
		var total = frm.doc.ecce + frm.doc.primary + frm.doc.post_primary;
		frm.set_value("total_rooms", total);
		if (total > frm.doc.total_rooms_school) {
			frappe.msgprint("Used classroom should be less or equal to the total rooms in the school")
			frm.set_value("total_rooms", '');
			frm.set_value("primary", '');
			frm.set_value("post_primary", '')
		}
	},
	post_primary: function (frm) {
		if (!Number.isInteger(frm.doc.post_primary)) {
			frm.set_value("post_primary", '')
		}
		if (frm.doc.post_primary < 0) {
			frm.set_value("post_primary", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.ecce) {
			frm.doc.ecce = 0;
		}
		if (!frm.doc.primary) {
			frm.doc.primary = 0;
		}
		if (!frm.doc.post_primary) {
			frm.doc.post_primary = 0;
		}
		var total = frm.doc.ecce + frm.doc.primary + frm.doc.post_primary;
		frm.set_value("total_rooms", total);
		if (total > frm.doc.total_rooms_school) {
			frappe.msgprint("Used classroom should be less or equal to the total rooms in the school")
			frm.set_value("total_rooms", '');
			frm.set_value("post_primary", '');
		}
	},
	adopted_school: function (frm) {
		if (frm.doc.adopted_school) {
			frm.set_value("adopter_name", '')
		}

	},
	is_this_branch_school: function (frm) {
		if (frm.doc.is_this_branch_school) {
			if (frm.doc.is_this_branch_school == 'Yes') {
				frm.set_df_property("semis", 'reqd', 1);
			}
			else {
				frm.set_df_property("semis", 'reqd', 0);
			}
			frm.set_value("name_of_main_school", '');
		}

	},
	is_work_done: function (frm) {
		if (frm.doc.is_work_done) {
			if (frm.doc.is_work_done == 'Yes') {
				//frm.set_df_property("what_constructed_in_school",'reqd', 1);
			}
			else {
				frm.set_df_property("what_constructed_in_school", 'reqd', 0);
			}
			frm.set_value("what_constructed_in_school", '');
			frm.set_value("what_constructed_text", '');
		}

	},
	is_campus_school: function (frm) {
		if (frm.doc.is_campus_school == "Yes" && frm.doc.semis_code) {
			cur_frm.clear_table("proforma_detail");
			frappe.call({
				method: "asc.asc.doctype.asc.asc.get_merged_schools",
				args: {
					semis_code: frm.doc.semis_code
				},
				callback: function (response) {
					frm.set_value("no_of_merger_schools", response.message.length_)
					var enrolment = response.message.enrolment;
					if (enrolment.length > 0) {
						var row = frappe.model.add_child(cur_frm.doc, "ASC", "proforma_detail");
						row.semis_code = frm.doc.semis_code;
						row.prefix = frm.doc.school_name;
						row.school_type = "CAMPUS";
						refresh_field("proforma_detail");
						for (let i = 0; i < enrolment.length; i++) {
							var row = frappe.model.add_child(cur_frm.doc, "ASC", "proforma_detail");
							row.semis_code = enrolment[i].semis_code;
							row.prefix = enrolment[i].school_name;
							row.school_type = "MERGED";
							refresh_field("proforma_detail");

						}
					}
				}
			})
		}
		else {
			frm.set_value("no_of_merger_schools", '')
			cur_frm.clear_table("proforma_detail");
		}

	},
	toilet_facility: function (frm) {
		if (frm.doc.toilet_facility) {
			frm.set_value("total_no_of_functional_toilets", '');
			frm.set_value("total_no_of_non_functional_toilet", '');
			frm.set_value("non_functional_toilet_reasons", '');
			frm.set_value("toilets_accessible_disabled", '');

		}
	},
	// wheel_chair_ramp_available:function(frm){
	// 	if(frm.doc.wheel_chair_ramp_available){
	// 		frm.set_value("polio_affected",'');
	// 		frm.set_value("physical_disabilites",'');
	// 		frm.set_value("total_disables",'');
	// 	}
	// },
	electricity_connection: function (frm) {
		if (frm.doc.electricity_connection) {
			frm.set_value("no_connection_reason", '');
			frm.set_value("status_of_electrification", '');
		}

	},
	mhm_facility: function (frm) {
		if (frm.doc.mhm_facility) {
			frm.set_value("disposal_for_sanitary", '');
		}

	},
	/*no_of_merger_schools:function(frm){
		if (!Number.isInteger(frm.doc.no_of_merger_schools)){
			frm.set_value("no_of_merger_schools",'')
		}
		if(frm.doc.no_of_merger_schools < 0 || frm.doc.no_of_merger_schools > 99){
				frm.set_value("no_of_merger_schools",'')
				frappe.msgprint("Value Must be between 1 to 99")
		}
	},*/
	total_no_of_functional_toilets: function (frm) {
		if (!Number.isInteger(frm.doc.total_no_of_functional_toilets)) {
			frm.set_value("total_no_of_functional_toilets", '')
		}
		if (frm.doc.total_no_of_functional_toilets < 0) {
			frm.set_value("total_no_of_functional_toilets", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (frm.doc.total_rooms_school && frm.doc.total_no_of_functional_toilets && frm.doc.total_rooms_school < frm.doc.total_no_of_functional_toilets) {
			frm.set_value("total_no_of_functional_toilets", '')
			frappe.msgprint("Total No Of Functional Toilets should be less or equal to the Total number of rooms in School")
		}
	},
	total_no_of_non_functional_toilet: function (frm) {
		if (!Number.isInteger(frm.doc.total_no_of_non_functional_toilet)) {
			frm.set_value("total_no_of_non_functional_toilet", '')
		}
		if (frm.doc.total_no_of_non_functional_toilet < 0) {
			frm.set_value("total_no_of_non_functional_toilet", '')
			frappe.msgprint("Must be a valid Number.")
		}
	},
	polio_affected: function (frm) {
		if (!Number.isInteger(frm.doc.polio_affected)) {
			frm.set_value("polio_affected", '')
		}
		if (frm.doc.polio_affected < 0) {
			frm.set_value("polio_affected", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.polio_affected) {
			frm.doc.polio_affected = 0;
		}
		if (!frm.doc.physical_disabilites) {
			frm.doc.physical_disabilites = 0;
		}
		var total = frm.doc.polio_affected + frm.doc.physical_disabilites
		frm.set_value("total_disables", total);
	},
	physical_disabilites: function (frm) {
		if (!Number.isInteger(frm.doc.physical_disabilites)) {
			frm.set_value("physical_disabilites", '')
		}
		if (frm.doc.physical_disabilites < 0) {
			frm.set_value("physical_disabilites", '')
			frappe.msgprint("Must be a valid Number.")
		}

		if (!frm.doc.polio_affected) {
			frm.doc.polio_affected = 0;
		}
		if (!frm.doc.physical_disabilites) {
			frm.doc.physical_disabilites = 0;
		}
		var total = frm.doc.polio_affected + frm.doc.physical_disabilites
		frm.set_value("total_disables", total);
	},
	govt_male_teachers: function (frm) {
		if (!Number.isInteger(frm.doc.govt_male_teachers)) {
			frm.set_value("govt_male_teachers", '')
		}
		if (frm.doc.govt_male_teachers < 0) {
			frm.set_value("govt_male_teachers", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.govt_male_teachers) {
			frm.doc.govt_male_teachers = 0;
		}
		if (!frm.doc.govt_female_teachers) {
			frm.doc.govt_female_teachers = 0;
		}
		if (!frm.doc.non_govt_male_teachers) {
			frm.doc.non_govt_male_teachers = 0;
		}
		if (!frm.doc.non_govt_female_teachers) {
			frm.doc.non_govt_female_teachers = 0;
		}
		var total_teachers =
			frm.doc.govt_male_teachers +
			frm.doc.govt_female_teachers +
			frm.doc.non_govt_male_teachers +
			frm.doc.non_govt_female_teachers;
		frm.set_value("total_teacher", total_teachers);
	},
	govt_female_teachers: function (frm) {
		if (!Number.isInteger(frm.doc.govt_female_teachers)) {
			frm.set_value("govt_female_teachers", '')
		}
		if (frm.doc.govt_female_teachers < 0) {
			frm.set_value("govt_female_teachers", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.govt_male_teachers) {
			frm.doc.govt_male_teachers = 0;
		}
		if (!frm.doc.govt_female_teachers) {
			frm.doc.govt_female_teachers = 0;
		}
		if (!frm.doc.non_govt_male_teachers) {
			frm.doc.non_govt_male_teachers = 0;
		}
		if (!frm.doc.non_govt_female_teachers) {
			frm.doc.non_govt_female_teachers = 0;
		}
		var total_teachers =
			frm.doc.govt_male_teachers +
			frm.doc.govt_female_teachers +
			frm.doc.non_govt_male_teachers +
			frm.doc.non_govt_female_teachers;
		frm.set_value("total_teacher", total_teachers);
	},
	non_govt_male_teachers: function (frm) {
		if (!Number.isInteger(frm.doc.non_govt_male_teachers)) {
			frm.set_value("non_govt_male_teachers", '')
		}
		if (frm.doc.non_govt_male_teachers < 0) {
			frm.set_value("non_govt_male_teachers", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.govt_male_teachers) {
			frm.doc.govt_male_teachers = 0;
		}
		if (!frm.doc.govt_female_teachers) {
			frm.doc.govt_female_teachers = 0;
		}
		if (!frm.doc.non_govt_male_teachers) {
			frm.doc.non_govt_male_teachers = 0;
		}
		if (!frm.doc.non_govt_female_teachers) {
			frm.doc.non_govt_female_teachers = 0;
		}
		var total_teachers =
			frm.doc.govt_male_teachers +
			frm.doc.govt_female_teachers +
			frm.doc.non_govt_male_teachers +
			frm.doc.non_govt_female_teachers;
		frm.set_value("total_teacher", total_teachers);
	},
	non_govt_female_teachers: function (frm) {
		if (!Number.isInteger(frm.doc.non_govt_male_teachers)) {
			frm.set_value("non_govt_male_teachers", '')
		}
		if (frm.doc.non_govt_male_teachers < 0) {
			frm.set_value("non_govt_male_teachers", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.govt_male_teachers) {
			frm.doc.govt_male_teachers = 0;
		}
		if (!frm.doc.govt_female_teachers) {
			frm.doc.govt_female_teachers = 0;
		}
		if (!frm.doc.non_govt_male_teachers) {
			frm.doc.non_govt_male_teachers = 0;
		}
		if (!frm.doc.non_govt_female_teachers) {
			frm.doc.non_govt_female_teachers = 0;
		}
		var total_teachers =
			frm.doc.govt_male_teachers +
			frm.doc.govt_female_teachers +
			frm.doc.non_govt_male_teachers +
			frm.doc.non_govt_female_teachers;
		frm.set_value("total_teacher", total_teachers);
	},
	non_teaching_male_staff: function (frm) {
		if (!Number.isInteger(frm.doc.non_teaching_male_staff)) {
			frm.set_value("non_teaching_male_staff", '')
		}
		if (frm.doc.non_teaching_male_staff < 0) {
			frm.set_value("non_teaching_male_staff", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.non_teaching_male_staff) {
			frm.doc.non_teaching_male_staff = 0;
		}
		if (!frm.doc.non_teaching_female_staff) {
			frm.doc.non_teaching_female_staff = 0;
		}
		var total_staff =
			frm.doc.non_teaching_male_staff + frm.doc.non_teaching_female_staff;
		frm.set_value("total_non_teaching_staff", total_staff);
	},
	non_teaching_female_staff: function (frm) {
		if (!Number.isInteger(frm.doc.non_teaching_female_staff)) {
			frm.set_value("non_teaching_female_staff", '')
		}
		if (frm.doc.non_teaching_female_staff < 0) {
			frm.set_value("non_teaching_female_staff", '')
			frappe.msgprint("Must be a valid Number.")
		}
		if (!frm.doc.non_teaching_male_staff) {
			frm.doc.non_teaching_male_staff = 0;
		}
		if (!frm.doc.non_teaching_female_staff) {
			frm.doc.non_teaching_female_staff = 0;
		}
		var total_staff =
			frm.doc.non_teaching_male_staff + frm.doc.non_teaching_female_staff;
		frm.set_value("total_non_teaching_staff", total_staff);
	},
	sindhi_medium_enrolment: function (frm) {
		if (!Number.isInteger(frm.doc.sindhi_medium_enrolment)) {
			frm.set_value("sindhi_medium_enrolment", '')
		}
		if (frm.doc.sindhi_medium_enrolment < 0) {
			frm.set_value("sindhi_medium_enrolment", '')
			frappe.msgprint("Must be a valid Number.")
		}
	},
	urdu_medium_enrolment: function (frm) {
		if (!Number.isInteger(frm.doc.urdu_medium_enrolment)) {
			frm.set_value("urdu_medium_enrolment", '')
		}
		if (frm.doc.urdu_medium_enrolment < 0) {
			frm.set_value("urdu_medium_enrolment", '')
			frappe.msgprint("Must be a valid Number.")
		}
	},
	english_medium_enrolment: function (frm) {
		if (!Number.isInteger(frm.doc.english_medium_enrolment)) {
			frm.set_value("english_medium_enrolment", '')
		}
		if (frm.doc.english_medium_enrolment < 0) {
			frm.set_value("english_medium_enrolment", '')
			frappe.msgprint("Must be a valid Number.")
		}
	},
	no_of_sef_schools: function (frm) {
		if (!Number.isInteger(frm.doc.no_of_sef_schools)) {
			frm.set_value("no_of_sef_schools", '')
		}
		if (frm.doc.no_of_sef_schools < 0 || frm.doc.no_of_sef_schools > 99) {
			frm.set_value("no_of_sef_schools", '')
			frappe.msgprint("Value Must be between 1 to 99")
		}
		if (!frm.doc.no_of_sef_schools) {
			frm.doc.no_of_sef_schools = 0;
		}
		if (!frm.doc.no_of_private_schools) {
			frm.doc.no_of_private_schools = 0;
		}
		var total_school = frm.doc.no_of_sef_schools + frm.doc.no_of_private_schools;
		frm.set_value("total_surrounding_schools", total_school)
	},
	no_of_private_schools: function (frm) {
		if (!Number.isInteger(frm.doc.no_of_private_schools)) {
			frm.set_value("no_of_private_schools", '')
		}
		if (frm.doc.no_of_private_schools < 0 || frm.doc.no_of_private_schools > 99) {
			frm.set_value("no_of_private_schools", '')
			frappe.msgprint("Value Must be between 1 to 99")
		}
		if (!frm.doc.no_of_sef_schools) {
			frm.doc.no_of_sef_schools = 0;
		}
		if (!frm.doc.no_of_private_schools) {
			frm.doc.no_of_private_schools = 0;
		}
		var total_school = frm.doc.no_of_sef_schools + frm.doc.no_of_private_schools;
		frm.set_value("total_surrounding_schools", total_school)
	},
	ddo_cost_center: function (frm) {
		if (frm.doc.ddo_cost_center && frm.doc.ddo_cost_center.length > 7) {
			var ddo_format = /^([a-zA-Z]{2}[\-][0-9]{4})$/;
			if (!(frm.doc.ddo_cost_center.match(ddo_format))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Format")
				frm.set_value("ddo_cost_center", '')
			}
		}

	},
	t_r_smc: function (frm) {
		if (frm.doc.t_r_smc) {
			if (String(frm.doc.t_r_smc).length > 6 || frm.doc.t_r_smc < 0) {
				frappe.msgprint("Please Enter Between 1 to 999,999")
				frm.set_value("t_r_smc", "");
			}
		}
	},
	utlized: function (frm) {
		if (frm.doc.utlized) {
			if (String(frm.doc.utlized).length > 6 || frm.doc.utlized < 0) {
				frappe.msgprint("Please Enter Between 1 to 999,999")
				frm.set_value("utlized", "");
			}
		}
	},
	m_repair: function (frm) {
		if (frm.doc.m_repair) {
			if (String(frm.doc.m_repair).length > 6 || frm.doc.m_repair < 0) {
				frappe.msgprint("Please Enter Between 1 to 999,999")
				frm.set_value("m_repair", "");
			}
		}
		if (!frm.doc.m_repair) {
			frm.doc.m_repair = 0;
		}
		if (!frm.doc.cleanliness) {
			frm.doc.cleanliness = 0;
		}
		if (!frm.doc.trans_for_g_c) {
			frm.doc.trans_for_g_c = 0;
		}
		var total = parseFloat(frm.doc.m_repair) + parseFloat(frm.doc.cleanliness) + parseFloat(frm.doc.trans_for_g_c);
		if (total > parseFloat(frm.doc.utlized)) {
			frappe.msgprint("Used Amount should be less or equal to the total Utilized Amount")
			frm.set_value("m_repair", '');
			frm.set_value("cleanliness", '');
			frm.set_value("trans_for_g_c", '');
		}
	},
	cleanliness: function (frm) {
		if (frm.doc.cleanliness) {
			if (String(frm.doc.cleanliness).length > 6 || frm.doc.cleanliness < 0) {
				frappe.msgprint("Please Enter Between 1 to 999,999")
				frm.set_value("cleanliness", "");
			}
		}
		if (!frm.doc.m_repair) {
			frm.doc.m_repair = 0;
		}
		if (!frm.doc.cleanliness) {
			frm.doc.cleanliness = 0;
		}
		if (!frm.doc.trans_for_g_c) {
			frm.doc.trans_for_g_c = 0;
		}
		var total = parseFloat(frm.doc.m_repair) + parseFloat(frm.doc.cleanliness) + parseFloat(frm.doc.trans_for_g_c);
		if (total > parseFloat(frm.doc.utlized)) {
			frappe.msgprint("Used Amount should be less or equal to the total Utilized Amount")
			frm.set_value("cleanliness", '');
			frm.set_value("trans_for_g_c", '');
		}
	},
	trans_for_g_c: function (frm) {
		if (frm.doc.trans_for_g_c) {
			if (String(frm.doc.trans_for_g_c).length > 6 || frm.doc.trans_for_g_c < 0) {
				frappe.msgprint("Please Enter Between 1 to 999,999")
				frm.set_value("trans_for_g_c", "");
			}
		}
		if (!frm.doc.m_repair) {
			frm.doc.m_repair = 0;
		}
		if (!frm.doc.cleanliness) {
			frm.doc.cleanliness = 0;
		}
		if (!frm.doc.trans_for_g_c) {
			frm.doc.trans_for_g_c = 0;
		}
		var total = parseFloat(frm.doc.m_repair) + parseFloat(frm.doc.cleanliness) + parseFloat(frm.doc.trans_for_g_c);
		if (total > parseFloat(frm.doc.utlized)) {
			frappe.msgprint("Used Amount should be less or equal to the total Utilized Amount")
			frm.set_value("trans_for_g_c", '');
		}
	},
	contact_no_enumerator: function (frm) {
		$("input[data-fieldname='contact_no_enumerator']").focusout(function () {
			var num = frm.doc.contact_no_enumerator
			if (!(phone_validate(num))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Enumerator phone number")
				frm.set_value("contact_no_enumerator", '')
			}
		});
	},
	cnic_no_enumerator: function (frm) {
		$("input[data-fieldname='cnic_no_enumerator']").focusout(function () {
			var cnic = frm.doc.cnic_no_enumerator
			if (!(cnic_validate(cnic))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Enumerator CNIC")
				frm.set_value("cnic_no_enumerator", '')
			}
		});
	},
	name_enumerator: function (frm) {
		$("input[data-fieldname='name_enumerator']").focusout(function () {
			var name = frm.doc.name_enumerator
			if (!(name_validate(name))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Enumerator Name")
				frm.set_value("name_enumerator", '')
			}
		});
	},

	contact_education_officer: function (frm) {
		$("input[data-fieldname='contact_education_officer']").focusout(function () {
			var num = frm.doc.contact_education_officer
			if (!(phone_validate(num))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Education Officer Phone")
				frm.set_value("contact_education_officer", '')
			}
		});
	},

	cnic_education_officer: function (frm) {
		$("input[data-fieldname='cnic_education_officer']").focusout(function () {
			var cnic = frm.doc.cnic_education_officer
			if (!(cnic_validate(cnic))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Education Officer CNIC")
				frm.set_value("cnic_education_officer", '')
			}
		});
	},

	name_education_officer: function (frm) {
		$("input[data-fieldname='name_education_officer']").focusout(function () {
			var name = frm.doc.name_education_officer
			if (!(name_validate(name))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Education Officer Name")
				frm.set_value("name_education_officer", '')
			}
		});
	},

	cnic_number_principal: function (frm) {
		$("input[data-fieldname='cnic_number_principal']").focusout(function () {
			var cnic = frm.doc.cnic_number_principal
			if (!(cnic_validate(cnic))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Principal CNIC")
				frm.set_value("cnic_number_principal", '')
			}
		});
	},
	principal_phone: function (frm) {
		$("input[data-fieldname='principal_phone']").focusout(function () {
			var num = frm.doc.principal_phone
			if (!(phone_validate(num))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Principal Phone")
				frm.set_value("principal_phone", '')
			}
		});
	},
	principal_hm_name: function (frm) {
		$("input[data-fieldname='principal_hm_name']").focusout(function () {
			var name = frm.doc.principal_hm_name
			if (!(name_validate(name))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Principal Name")
				frm.set_value("principal_hm_name", '')
			}
		});
	},
	principal_email: function (frm) {
		$("input[data-fieldname='principal_email']").focusout(function () {
			var email = frm.doc.principal_email
			if (!(email_validate(email))) {
				$(".msgprint").empty()
				frappe.msgprint("Please Enter valid Principal Email")
				frm.set_value("principal_email", '')
			}
		});
	},
	source_drinking_water: function (frm) {
		var element = false
		const doc = frm.doc.source_drinking_water
		for (var i = 0; i < doc.length; i++) {
			if (doc[i]['name1'] == 'No Water') {
				element = true;
			}
		}
		if (element) {
			frm.set_df_property('provision_drinking_water', 'hidden', 1);
			frm.set_value('provision_drinking_water', '');
		}
		else {
			frm.set_df_property('provision_drinking_water', 'hidden', 0);
		}
	},
	refresh: function (frm) {
		var is_allowed = frappe.user_roles.includes('System Manager');
		if (is_allowed == false) {
			frm.set_df_property('year', 'read_only', 1);
			frm.set_df_property('reference_date', 'read_only', 1);
		}
		else {
			frm.set_df_property('year', 'read_only', 0);
		}

		frappe.call({
			method: "asc.asc.doctype.asc.asc.select_values",
			async: false,
			callback: function (r) {
				var return_data = r.message;
				for (var key in return_data) {
					var type = [""]
					var others_ = ""
					var data_ = return_data[key];
					for (var i = 0; i < data_.length; i++) {
						if (data_[i] == "Other" || data_[i] == "Others" || data_[i] == "Any Other Reason(s)") {
							others_ = "Other"
							if (data_[i] == 'Others') {
								others_ = "Others"
							}
							if (data_[i] == "Any Other Reason(s)") {
								others_ = "Any Other Reason(s)"
							}

						}
						else {
							type.push(data_[i]);
						}

					}
					if (String(others_).length > 0) {
						type.push(others_)
					}

					frm.set_df_property(String(key), "options", type);
					frm.refresh_field(String(key));
				}
			}
		});

	},
	onload: function (frm) {
		if (frm.doc.completion_check && frappe.user_roles.includes('Data Entry Operator') && !(frappe.user_roles.includes('System Manager'))) {
			for (let i = 0; i < asc_fields.length; i++) {
				frm.set_df_property(asc_fields[i], "read_only", 1);
			}
		}
		/*else {
			for (let i = 0; i < asc_fields.length; i++) {
				frm.set_df_property(asc_fields[i], "read_only", 0);
			}
		}*/
		//frm.get_field("gender_wise_enrolment").grid.cannot_add_rows = true;
		//frm.get_field("table_repeaters").grid.cannot_add_rows = true;
		//frm.get_field("status_items_availability").grid.cannot_add_rows = true;	
		//frm.get_field("status_of_facilities_availability").grid.cannot_add_rows = true;	
		//frm.get_field("proforma_detail").grid.cannot_add_rows = true;
		frappe.call({
			method: "asc.asc.doctype.asc.asc.get_defaults",
			callback: function (r) {
				if (frm.is_new()) {
					frm.set_value("reference_date", r.message[0])
					frm.set_value("year", r.message[1])
					frm.set_value("visit_date_and_time", r.message[2])
				}
				var html_ = "<h2 style='text-align: center;'> Annual School Census " + String(r.message[1]) + "</h2>"
				$(frm.fields_dict.html_2.wrapper).empty();
				$(html_).appendTo(frm.fields_dict.html_2.wrapper);
			}
		});

		$("input[data-fieldname='contact_no_enumerator']").mask('0000-0000000');
		//$("input[data-fieldname='school_phone_no']").mask('0000-0000000');
		$("input[data-fieldname='cnic_no_enumerator']").mask('00000-0000000-0');
		$("input[data-fieldname='cnic_number_principal']").mask('00000-0000000-0');
		$("input[data-fieldname='contact_education_officer']").mask('0000-0000000');
		$("input[data-fieldname='cnic_education_officer']").mask('00000-0000000-0');
		$("input[data-fieldname='principal_phone']").mask('0000-0000000');
		$("input[data-fieldname='ddo_cost_center']").mask('SS-0000');

		frm.set_query("district", function () {

			return {
				"filters": {
					"division": frm.doc.region
				}
			};
		});
		frm.set_query("taluka", function () {
			return {
				"filters": {
					"district": frm.doc.district
				}
			}
		});
		frm.set_query("uc", function () {
			return {
				"filters": {
					"taluka_name": frm.doc.taluka
				}
			}
		});
		$(".like-disabled-input").children().bind('click', function () { return false; });

		$(".like-disabled-input a").click(function (e) {
			$(".like-disabled-input a").attr('href', "javascript: void(0);");
			e.preventDefault();

			return false;
		});//.off("click").attr('href', "javascript: void(0);");
	},
	validate: function (frm) {
		if (frm.doc.completion_check && frappe.user_roles.includes('Data Entry Operator') && !(frappe.user_roles.includes('System Manager'))) {
			frappe.confirm(__('Are you sure you want to send this to LSU for Verification?'),
				function () {
					if (frm.doc.total_teacher != frm.doc.staff_detail.length) {
						frm.set_value("completion_check", 0)
						frappe.throw("The no. of teachers you entered do not match total teachers")
					} else {
						for (let i = 0; i < asc_fields.length; i++) {
							frm.set_df_property(asc_fields[i], "read_only", 1);
						}
					}
				}
			);
		} else {
			for (let i = 0; i < asc_fields.length; i++) {
				frm.set_df_property(asc_fields[i], "read_only", 0);
			}
		}
	}


});

frappe.ui.form.on("Status of Items availability", {
	working: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!doc.working) {
			doc.working = 0;
		}
		if (!doc.repairable) {
			doc.repairable = 0;

		}
		var full = doc.working + doc.repairable;
		frappe.model.set_value(cdt, cdn, "total", full);
	},
	repairable: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!doc.repairable) {
			doc.repairable = 0;
		}
		if (!doc.working) {
			doc.working = 0;

		}
		var full = doc.working + doc.repairable;
		frappe.model.set_value(cdt, cdn, "total", full);
	},

})

frappe.ui.form.on("Enrolment Class and Gender wise", {
	boys: function (frm, cdt, cdn) {
		var temp = 0;
		var doc = locals[cdt][cdn];
		if (!doc.boys) {
			doc.boys = 0;
		}
		if (!doc.girls) {
			doc.girls = 0;
		}
		var full_class = doc.boys + doc.girls;

		frappe.model.set_value(cdt, cdn, "total_class", full_class);

		var loop_data = frm.doc.gender_wise_enrolment;
		for (var x = 0; x < loop_data.length; x++) {
			if (!loop_data[x]["boys"]) {
				loop_data[x]["boys"] = 0;
			}
			if (!loop_data[x]["girls"]) {
				loop_data[x]["girls"] = 0;
			}
			var full_class = loop_data[x]["boys"] + loop_data[x]["girls"];
			temp = temp + full_class;

		}
		frappe.model.set_value(cdt, cdn, "overall_total", temp);
	},
	girls: function (frm, cdt, cdn) {
		var temp = 0;
		var doc = locals[cdt][cdn];
		if (!doc.girls) {
			doc.girls = 0;
		}
		if (!doc.boys) {
			doc.boys = 0;
		}
		var full_class = doc.boys + doc.girls;
		frappe.model.set_value(cdt, cdn, "total_class", full_class);

		var loop_data = frm.doc.gender_wise_enrolment;
		for (var x = 0; x < loop_data.length; x++) {
			if (!loop_data[x]["boys"]) {
				loop_data[x]["boys"] = 0;
			}
			if (!loop_data[x]["girls"]) {
				loop_data[x]["girls"] = 0;
			}
			var full_class = loop_data[x]["boys"] + loop_data[x]["girls"];
			temp = temp + full_class;

		}
		frappe.model.set_value(cdt, cdn, "overall_total", temp);
	},
});

frappe.ui.form.on("Repeaters", {
	boys: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!doc.girls) {
			doc.girls = 0;
		}
		if (!doc.boys) {
			doc.boys = 0;
		}
		var fullclass = doc.boys + doc.girls;
		frappe.model.set_value(cdt, cdn, "total", fullclass);
		temp = temp + fullclass;
		frappe.model.set_value(cdt, cdn, "overall", temp);
	},
	girls: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!doc.girls) {
			doc.girls = 0;
		}
		if (!doc.boys) {
			doc.boys = 0;
		}
		var fullclass = doc.boys + doc.girls;
		frappe.model.set_value(cdt, cdn, "total", fullclass);
		temp = temp + fullclass;
		frappe.model.set_value(cdt, cdn, "overall", temp);
	},
});

frappe.ui.form.on("Surrounding Government Schools", {
	semis_code: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!Number.isInteger(doc.semis_code)) {
			frappe.model.set_value(cdt, cdn, "semis_code", "")
		}
		if (doc.semis_code < 0) {
			frappe.model.set_value(cdt, cdn, "semis_code", "")
			frappe.msgprint("Must be a valid Number.")
		}
		if (doc.semis_code && frm.doc.district) {
			frappe.call({
				method: "asc.asc.doctype.asc.asc.share_semis_code",
				args: {
					semis_code: doc.semis_code,
					district: frm.doc.district,
					main_semis: frm.doc.semis_code
				},
				callback: function (r) {
					if (r.message == 1) {
						frappe.model.set_value(cdt, cdn, "semis_code", "")
						frappe.msgprint("District should be same for both schools")
					}

					if (r.message[0] == 1) {
						frappe.model.set_value(cdt, cdn, "semis_code", "")
						frappe.model.set_value(cdt, cdn, "school_name_prefix_and_name)", "");
						frappe.msgprint("District should be same for both schools")
					}
					else {
						frappe.model.set_value(cdt, cdn, "school_name_prefix_and_name", r.message[1]);
					}
				}
			});
		}

	},
	type_of_school_see_codes: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (doc.type_of_school_see_codes) {
			frappe.model.set_value(cdt, cdn, "distance_in_meters", "")
		}

	},
	distance_in_meters: function (frm, cdt, cdn) {
		var doc = locals[cdt][cdn];
		if (!Number.isInteger(doc.distance_in_meters)) {
			frappe.model.set_value(cdt, cdn, "distance_in_meters", "")
		}
		if ((doc.distance_in_meters < 0 || doc.distance_in_meters > 500) && doc.type_of_school_see_codes == 'Within 500 Meters') {
			frappe.model.set_value(cdt, cdn, "distance_in_meters", "")
			frappe.msgprint("Distance must be between 1 to 500 meters")
		}

	},
});



