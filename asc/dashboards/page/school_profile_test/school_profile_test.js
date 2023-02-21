frappe.pages['school-profile-test'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'School Profile',
		single_column: true
	});
	filters.add(page);
}

filters = {
	add: function (page) {
		let set_route_year = frappe.get_route()[1]
		let set_route_school = frappe.get_route()[2]
		let school
		let year
		if (!set_route_year) {
			year = page.add_field({
				label: "Year",
				fieldtype: "Link",
				fieldname: "Year",
				options: "Year",
				default: "2021-22",
				reqd: 1
			});
		} else {
			year = page.add_field({
				label: "Year",
				fieldtype: "Link",
				fieldname: "Year",
				options: "Year",
				default: `${set_route_year}`,
				reqd: 1
			});
		}

		if (!set_route_school) {
			school = page.add_field({
				label: "School",
				fieldtype: "Link",
				fieldname: "school",
				options: "School",
				reqd: 1,
				// "onchange": function() {
				// 	const year_ = year.get_value()
				// 	const school_ = school.get_value()
				// 	if (school_ == "" || year_ == "") {
				// 		return;
				// 	}
				// 	server_call(page, school_, year_)
				// }
			});
		} else {
			school = page.add_field({
				label: "School",
				fieldtype: "Link",
				fieldname: "school",
				options: "School",
				default: `${set_route_school}`,
				reqd: 1,
				// 	"onchange": function() {
				// 	const year_ = year.get_value()
				// 	const school_ = school.get_value()
				// 	if (school_ == "" || year_ == "") {
				// 		return;
				// 	}
				// 	server_call(page, school_, year_)
				// }
			});
		}

		let fiterbtn = page.add_field({
			label: "View",
			fieldtype: "Button",
			fieldname: "filter",
			click() {
				const year_ = year.get_value()
				const school_ = school.get_value()
				if (year_ == "" || school_ == "") {
					return;
				}
				$('#school_profile').remove();
				$(
					frappe.render_template("school_skeleton")
				).appendTo(page.main);
				server_call(page, school_, year_)


				// if (school.get_value() == "" || year.get_value() == "") {
				// 	return;
				// }
				// $('#loader').remove();
				// var img = $('<img />', {
				// 	id: 'loader',
				// 	src: '/assets/img/loading.gif',
				// 	alt: 'Loading',
				// 	style: 'text-align:center; margin:0 auto; display:block'
				// });
				// img.appendTo(page.main);
				// $('#school_profile').remove();
				// frappe.call({
				// 	method: "asc.dashboards.page.school_profile_test.school_profile_test.get_data",
				// 	args: {
				// 		school: school.get_value(),
				// 		year: year.get_value(),
				// 	},
				// 	callback: function (r) {
				// 		$('#loader').remove();
				// 		$('#school_profile').remove();
				// 		if (r.message == 1) {
				// 			frappe.msgprint("No Data Found")
				// 		} else {
				// 			$(
				// 				frappe.render_template("school_profile_test", { 'response': r.message })
				// 			).appendTo(page.main);
				// 		}
				// 	},
				// });
			},//end of click
		});//end of view-btn
	},//end of add
};//end of filters

async function server_call(page, school_, year_) {

	var not_exist_flag = false
	var sec_flag = false
	var hi_sec_flag = false
	//call for basic data
	await frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.basic_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {
			console.log(r.message);
			data = r.message[0]
			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#basic_data').empty();

				$(
					frappe.render_template("basic_data_school", r.message[0])
				).appendTo("#basic_data");

				if (data.reason == "School does not exist") {
					not_exist_flag = true
					$('#tab_buttons').empty();
					$('#visit-section').empty();
					$('#building_info').empty();
					$('#staff_data').empty();
					$('#facility_data').empty();
					$('#item_data').empty();
					$('#enrollment_data').empty();
					$('#secondary_data').empty();
					$('#hi_secondary_data').empty();
					$('#smc_section').empty();
					return
				}
				if (data.level == "Secondary") {
					sec_flag = true;
					$('#hi_secondary_data').empty();
				} else if (data.level == "Higher Secondary") {
					hi_sec_flag = true;
				} else {
					$('#secondary_data').empty();
					$('#hi_secondary_data').empty();
				}

				$('#tab_buttons').empty();
				$(
					frappe.render_template("buttons", r.message[0])
				).appendTo("#tab_buttons");


				$('.nav-tabs button').click(function () {
					$("#asc-section").removeClass('active');
					$("#visit-section").removeClass('active');
					$("#asc-section-tab").removeClass('active');
					$("#visit-section-tab").removeClass('active');

					$("#asc-section").removeClass('show');
					$("#visit-section").removeClass('show');
					var target = $(this).data('bs-target');
					console.log("target", target);
					$(target).tab('show');
					$(target + '-tab').addClass('active');
				})
			}
		},
	});//call for basic data

	if (not_exist_flag) {
		not_exist_flag = false
		return
	}

	//call for visit-section
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.visit_section",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {
			console.log(r.message);
			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#visit-section').empty();

				$(
					frappe.render_template("mne_tab", r.message[0])
				).appendTo("#visit-section");
			}
		},
	});//call for visit-section

	//call for building_data
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.building_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {
			// console.log(r.message);
			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#building_info').empty();

				$(
					frappe.render_template("building_data", r.message[0])
				).appendTo("#building_info");
			}
		},
	});//call for building_data


	//call for staff
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.staff_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {

			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#staff_data').empty();

				$(
					frappe.render_template("staff_data", r.message[0])
				).appendTo("#staff_data");
			}
		},
	});//call for staff_data

	//call for facility_data
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.facility_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {

			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#facility_data').empty();

				$(
					frappe.render_template("facility_data", r.message[0])
				).appendTo("#facility_data");
			}
		},
	});//call for facility_data

	//call for item_data
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.item_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {

			if (r.message == 1) {
				$('#item_data').empty();

			} else {
				$('#item_data').empty();

				$(
					frappe.render_template("item_data", r.message[0])
				).appendTo("#item_data");
			}
		},
	});//call for item_data

	//call for enrollment
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.enrollment_data",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {

			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#enrollment_data').empty();

				$(
					frappe.render_template("enrollment_data", r.message[0])
				).appendTo("#enrollment_data");
			}
		},
	});//call for enrollment

	if (sec_flag || hi_sec_flag) {
		//call for secondary_data
		frappe.call({
			method: "asc.dashboards.page.school_profile_test.school_profile_test.secondary_data",
			args: {
				school: school_,
				year: year_,
			},
			callback: function (r) {

				if (r.message == 1) {
					frappe.msgprint("No Data Found")
				} else {
					$('#secondary_data').empty();

					$(
						frappe.render_template("secondary_data", r.message[0])
					).appendTo("#secondary_data");
				}
			},
		});//call for secondary_data
	}

	if (hi_sec_flag) {
		//call for hi_secondary_data
		frappe.call({
			method: "asc.dashboards.page.school_profile_test.school_profile_test.hi_secondary_data",
			args: {
				school: school_,
				year: year_,
			},
			callback: function (r) {

				if (r.message == 1) {
					frappe.msgprint("No Data Found")
				} else {
					$('#hi_secondary_data').empty();

					$(
						frappe.render_template("hi_secondary_data", r.message[0])
					).appendTo("#hi_secondary_data");
				}
			},
		});//call for hi_secondary_data
	}
	//call for smc_section
	frappe.call({
		method: "asc.dashboards.page.school_profile_test.school_profile_test.smc_section",
		args: {
			school: school_,
			year: year_,
		},
		callback: function (r) {

			if (r.message == 1) {
				frappe.msgprint("No Data Found")
			} else {
				$('#smc_section').empty();

				$(
					frappe.render_template("smc_section", r.message[0])
				).appendTo("#smc_section");
			}
		},
	});//call for smc_section
}