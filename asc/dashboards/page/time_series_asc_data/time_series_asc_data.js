frappe.require([
	'/assets/semis_theme/js/export_custom.js',
]);
frappe.pages['time-series-asc-data'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Time Series ASC Data',
		single_column: true
	});
	// $(frappe.render_template('time_series_asc_data')).appendTo(page.main);
	//draw_map();
	filters.add(page);
	wrapper.page.add_inner_button(__('Export'), () => {
		downloadtable("#time_series_asc_data", "Time Series ASC Data")
	});
}
filters = {
	add: async function (page) {
		let division
		let district
		let district_by_user
		let division_by_user
		let read_only = false;
		var system_manager = frappe.user_roles.includes('System Manager');
		var lsu = frappe.user_roles.includes('LSU');

		if (lsu == true && system_manager == false) {
			await frappe.call({
				method: "frappe.smc.page.smc_dashboard.smc_dashboard.district_for_lsu",
				args: { user: frappe.session.user },
				callback: function (r) {
					console.log(r.message);
					division_by_user = r.message[1].division;
					district_by_user = r.message[0].district;
					read_only = true;
				}
			});
		}
		else {
			division_by_user = '';
			district_by_user = '';
		}

		if (read_only == true) {
			division = page.add_field({
				label: "Division",
				fieldtype: "Link",
				fieldname: "division",
				options: "Division",
				read_only: 1,
				default: `${division_by_user}`,
			});
			district = page.add_field({
				label: "District",
				fieldtype: "Link",
				fieldname: "district",
				options: "District",
				read_only: 1,

				default: `${district_by_user}`,
				"get_query": function () {
					if (!school.get_value()) {
						return
					}
					else {
						return {
							"filters": { "district": district.get_value() }
						}
					}
				},
				read_only: 1
			});

		}
		else {
			division = page.add_field({
				label: "Division",
				fieldtype: "Link",
				fieldname: "division",
				options: "Division",
			});
			district = page.add_field({
				label: "District",
				fieldtype: "Link",
				fieldname: "district",
				options: "District",
				default: `${district_by_user}`,
				"get_query": function () {
					return {
						"filters": {
							"division": division.get_value("division"),
						}
					}
				}
			});
		}
		let taluka = page.add_field({
			"label": "Taluka",
			"fieldtype": "Link",
			"fieldname": "taluka",
			"options": "Taluka",
			"hidden": 1,
			"get_query": function () {
				return {
					"filters": {
						"district": district.get_value("district"),
					}
				}
			},
			"onchange": function () {
				// page_data(page, division.get_value(), district.get_value(), taluka.get_value(), level.get_value()) 
			}
		});
		let level = page.add_field({
			"label": "Level",
			"fieldtype": "Link",
			"fieldname": "level",
			"options": "Level",
			"onchange": function () {
				// page_data(page, division.get_value(), district.get_value(), taluka.get_value(), level.get_value()) 
			}
		});
		let fiterbtn = page.add_field({
			label: "View",
			fieldtype: "Button",
			fieldname: "filter",
			async click() {
				page_data(page, division.get_value(), district.get_value(), taluka.get_value(), level.get_value())
			},
		});
		page_data(page, division.get_value(), district.get_value(), taluka.get_value(), level.get_value())
	}
}
function page_data(page, division, district, taluka, level) {
	frappe.call({
		method: "asc.dashboards.page.time_series_asc_data.time_series_asc_data.get_data",
		args: {
			district: district,
			division: division,
			taluka: taluka,
			level: level
		},
		freeze: true,
		callback: function (r) {
			console.log("res", r.message);

			var data = r.message[0].reverse()
			var span = r.message[1];
			console.log("Response", data);
			$('#time_series_asc_data').remove();
			$(frappe.render_template("time_series_asc_data", { "data": data, "span": span })).appendTo(page.main);
		}
	});
}