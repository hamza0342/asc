let year = null;
let five_years = null;
var pivot = null;
var pivotoption = null;
var pivotcolumns = null;
var jsonData = null;

frappe.pages['pivot-table'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Pivot Table',
		single_column: true
	});
	$(frappe.render_template("pivot_table")).appendTo(page.main);


	// pivot_table('2021-22', 0)
	filters.add(page);

	// //save button
	wrapper.page.add_inner_button(__('Save'), () => {
		pivotoption = pivot.getOptions();
		pivotcolumns = pivot.getReport({
			withGlobals: true,
			withDefaults: true
		});


		current_user = frappe.session.user
		pivotcolumns.dataSource.data = new Array();
		frappe.prompt([
			{
				label: 'Report Name',
				fieldname: 'report_name',
				fieldtype: 'Data',
				reqd: 1
			},
			{
				label: 'Save as',
				fieldname: 'option',
				fieldtype: 'Select',
				default: 'Private',
				options: ["Public", "Private"]
			},
		], (values) => {

			frappe.call({
				method: "asc.dashboards.page.pivot_table.pivot_table.save_data",
				args: {
					report_name: values.report_name,
					option: values.option,
					current_user: current_user,
					year: year.get_value(),
					last_five_years: five_years.get_value(),
					pivot_options: JSON.stringify(pivotoption),
					pivot_columns: JSON.stringify(pivotcolumns),
				},
				freeze: true,
				callback: function (r) {
					if (r.message == 1) {
						pivotcolumns.dataSource.data = jsonData;
						frappe.show_alert({
							message: __('Saved'),
							indicator: 'green'
						}, 5);
					}

				}
			});
		})

	});//end


	//open button
	wrapper.page.add_inner_button(__('Open Report'), async () => {

		current_user = frappe.session.user
		var report_names = null;


		await frappe.call({
			method: "asc.dashboards.page.pivot_table.pivot_table.report_names",
			args: {
				current_user: current_user,
			},
			freeze: true,
			callback: function (r) {
				console.log("test", r.message);
				report_names = r.message;
			}
		});
		console.log("test", report_names);

		frappe.prompt([
			{
				label: 'Report Name',
				fieldname: 'report_name',
				fieldtype: 'Select',
				options: report_names,
				reqd: 1
			},
		], (values) => {

			frappe.call({
				method: "asc.dashboards.page.pivot_table.pivot_table.get_report",
				args: {
					report_name: values.report_name,
				},
				freeze: true,
				callback: function (r) {
					pivotoption = JSON.parse(r.message[0]);
					pivotcolumns = JSON.parse(r.message[1]);

					load_table(r.message[2]);
				}
			});
		})



	});//end




}


filters = {
	add: function (page) {
		year = page.add_field({
			label: "Year",
			fieldtype: "Link",
			fieldname: "Year",
			options: "Year",
			default: "2021-22",
			change() {
				if (five_years.get_value() == 1 && year.get_value() != "") {
					five_years.set_value(0);
				}
			},
		});
		five_years = page.add_field({
			label: "Last 5 census",
			fieldtype: "Check",
			fieldname: "five_years",
			change() {
				if (year.get_value() != "" && five_years.get_value() == 1) {
					year.set_value("");
				}
			},
		});
		let fiterbtn = page.add_field({
			label: "Load",
			fieldtype: "Button",
			fieldname: "filter",
			click() {
				pivot_table(year.get_value(), five_years.get_value())
			},
		});
		// let save = page.add_field({
		// 	label: "Save",
		// 	fieldtype: "Button",
		// 	fieldname: "save_button",
		// 	click() {
		// 		pivotoption = pivot.getOptions();
		// 		pivotcolumns = pivot.getReport({
		// 			withGlobals: true,
		// 			withDefaults: true
		// 		});


		// 		current_user = frappe.session.user
		// 		pivotcolumns.dataSource.data = new Array();
		// 		frappe.prompt([
		// 			{
		// 				label: 'Report Name',
		// 				fieldname: 'report_name',
		// 				fieldtype: 'Data',
		// 				reqd: 1
		// 			},
		// 			{
		// 				label: 'Save as',
		// 				fieldname: 'option',
		// 				fieldtype: 'Select',
		// 				default: 'Private',
		// 				options: ["Public", "Private"]
		// 			},
		// 		], (values) => {

		// 			frappe.call({
		// 				method: "asc.dashboards.page.pivot_table.pivot_table.save_data",
		// 				args: {
		// 					report_name: values.report_name,
		// 					option: values.option,
		// 					current_user: current_user,
		// 					year: year.get_value(),
		// 					last_five_years: five_years.get_value(),
		// 					pivot_options: JSON.stringify(pivotoption),
		// 					pivot_columns: JSON.stringify(pivotcolumns),
		// 				},
		// 				freeze: true,
		// 				callback: function (r) {
		// 					if (r.message == 1) {
		// 						pivotcolumns.dataSource.data = jsonData;
		// 						frappe.show_alert({
		// 							message: __('Saved'),
		// 							indicator: 'green'
		// 						}, 5);
		// 					}

		// 				}
		// 			});
		// 		})
		// 	},
		// });
		// let load_report = page.add_field({
		// 	label: "Open Report",
		// 	fieldtype: "Button",
		// 	fieldname: "load_report",
		// 	async click() {
		// 		current_user = frappe.session.user
		// 		var report_names = null;


		// 		await frappe.call({
		// 			method: "asc.dashboards.page.pivot_table.pivot_table.report_names",
		// 			args: {
		// 				current_user: current_user,
		// 			},
		// 			freeze: true,
		// 			callback: function (r) {
		// 				report_names = r.message;
		// 			}
		// 		});

		// 		frappe.prompt([
		// 			{
		// 				label: 'Report Name',
		// 				fieldname: 'report_name',
		// 				fieldtype: 'Select',
		// 				options: report_names,
		// 				reqd: 1
		// 			},
		// 		], (values) => {

		// 			frappe.call({
		// 				method: "asc.dashboards.page.pivot_table.pivot_table.get_report",
		// 				args: {
		// 					report_name: values.report_name,
		// 				},
		// 				freeze: true,
		// 				callback: function (r) {
		// 					pivotoption = JSON.parse(r.message[0]);
		// 					pivotcolumns = JSON.parse(r.message[1]);

		// 					load_table(r.message[2]);
		// 				}
		// 			});
		// 		})
		// 	},
		// });
	},
};

async function load_table(years) {
	var years_ = years.year;
	var fiveyears = years.last_five_years;
	year.set_value(years_)
	five_years.set_value(fiveyears)

	if (!pivot) {
		await pivot_table(years_, fiveyears)

		pivot.setOptions(pivotoption);
		pivot.setReport(pivotcolumns);
		pivot.refresh();
	}


	frappe.call({
		method: "asc.dashboards.page.pivot_table.pivot_table.get_data",
		args: {
			year: years_,
			five_years: fiveyears,

		},
		freeze: true,
		callback: function (r) {

			var jsonData = r.message;
			pivot.setOptions(pivotoption);
			pivot.setReport(pivotcolumns);
			pivot.updateData({ data: jsonData });
			pivot.refresh();
		}
	});
}

async function pivot_table(year, five_years) {
	await frappe.call({
		method: "asc.dashboards.page.pivot_table.pivot_table.get_data",
		args: {
			year: year,
			five_years: five_years,
		},
		freeze: true,
		callback: function (r) {

			var data = r.message;
			jsonData = r.message;

			if (pivot) {
				console.log("if", jsonData);
				pivot.updateData({ data: jsonData });
				pivot.refresh();
			} else {
				console.log("else");

				pivot = new Flexmonster({
					container: "#pivot-container",
					componentFolder: "https://cdn.flexmonster.com/",
					width: "100%",
					height: "70vh",
					toolbar: true,
					beforetoolbarcreated: customizeToolbar,
					report: {
						"dataSource": {
							type: "json",
							data: data,
							mapping: {
								"SEMIS Code": {
									"caption": "SEMIS Code",
									"type": "string"
								},
								"Year": {
									"caption": "Year",
									"type": "string"
								},
								"Division": {
									"caption": "Division",
									"type": "string"
								},
								"District": {
									"caption": "District",
									"type": "string"
								},
								"Tehsil": {
									"caption": "Tehsil",
									"type": "string"
								},
								"UC": {
									"caption": "UC",
									"type": "string"
								},
								"School Name": {
									"caption": "School Name",
									"type": "string"
								},
								"Location": {
									"caption": "Location",
									"type": "string"
								},
								"Gender": {
									"caption": "Gender",
									"type": "string"
								},
								"Level": {
									"caption": "Level",
									"type": "string"
								},
								"Status": {
									"caption": "Status",
									"type": "string"
								},
								"Closure Period": {
									"caption": "Closure Period",
									"type": "string"
								},
								"Closure Reason": {
									"caption": "Closure Reason",
									"type": "string"
								},
								"Building Availability": {
									"caption": "Building Availability",
									"type": "string"
								},
								"Building Ownership": {
									"caption": "Building Ownership",
									"type": "string"
								},
								"Building Condition": {
									"caption": "Building Condition",
									"type": "string"
								},
								"Water": {
									"caption": "Water",
									"type": "string"
								},
								"Electricity": {
									"caption": "Electricity",
									"type": "string"
								},
								"Toilet": {
									"caption": "Toilet",
									"type": "string"
								},
								"Condition of Boundary Wall": {
									"caption": "Condition of Boundary Wall",
									"type": "string"
								},
								"Rooms": {
									"caption": "Rooms",
									"type": "number"
								},
								"Post Primary": {
									"caption": "Post Primary",
									"type": "number"
								},
								"Primary": {
									"caption": "Primary",
									"type": "number"
								},
								"ECCE": {
									"caption": "ECCE",
									"type": "number"
								},
								"Classrooms": {
									"caption": "Classrooms",
									"type": "number"
								},
								"Total Teachers": {
									"caption": "Total Teachers",
									"type": "number"
								},
								"Female Teachers": {
									"caption": "Female Teachers",
									"type": "number"
								},
								"Male Teachers": {
									"caption": "Male Teachers",
									"type": "number"
								},
								"English Enrollment": {
									"caption": "English Enrollment",
									"type": "number"
								},
								"Urdu Enrollment": {
									"caption": "Urdu Enrollment",
									"type": "number"
								},
								"Sindhi Enrollment": {
									"caption": "Sindhi Enrollment",
									"type": "number"
								},
								"Girls Enrollment": {
									"caption": "Girls Enrollment",
									"type": "number"
								},
								"Boys Enrollment": {
									"caption": "Boys Enrollment",
									"type": "number"
								},
								"Total Enrollment": {
									"caption": "Total Enrollment",
									"type": "number"
								},
								"ECCE Male": {
									"caption": "ECCE Male",
									"type": "number"
								},
								"ECCE Female": {
									"caption": "ECCE Female",
									"type": "number"
								},
								"Katchi Male": {
									"caption": "Katchi Male",
									"type": "number"
								},
								"Katchi Female": {
									"caption": "Katchi Female",
									"type": "number"
								},
								"Class-I Male": {
									"caption": "Class-I Male",
									"type": "number"
								},
								"Class-I Female": {
									"caption": "Class-I Female",
									"type": "number"
								},
								"Class-II Male": {
									"caption": "Class-II Male",
									"type": "number"
								},
								"Class-II Female": {
									"caption": "Class-II Female",
									"type": "number"
								},
								"Class-III Male": {
									"caption": "Class-III Male",
									"type": "number"
								},
								"Class-III Female": {
									"caption": "Class-III Female",
									"type": "number"
								},
								"Class-IV Male": {
									"caption": "Class-IV Male",
									"type": "number"
								},
								"Class-IV Female": {
									"caption": "Class-IV Female",
									"type": "number"
								},
								"Class-V Male": {
									"caption": "Class-V Male",
									"type": "number"
								},
								"Class-V Female": {
									"caption": "Class-V Female",
									"type": "number"
								},
								"Class-VI Male": {
									"caption": "Class-VI Male",
									"type": "number"
								},
								"Class-VI Female": {
									"caption": "Class-VI Female",
									"type": "number"
								},
								"Class-VII Male": {
									"caption": "Class-VII Male",
									"type": "number"
								},
								"Class-VII Female": {
									"caption": "Class-VII Female",
									"type": "number"
								},
								"Class-VIII Male": {
									"caption": "Class-VIII Male",
									"type": "number"
								},
								"Class-VIII Female": {
									"caption": "Class-VIII Female",
									"type": "number"
								},
								"Class-IX Male": {
									"caption": "Class-IX Male",
									"type": "number"
								},
								"Class-IX Female": {
									"caption": "Class-IX Female",
									"type": "number"
								},
								"Class-X Male": {
									"caption": "Class-X Male",
									"type": "number"
								},
								"Class-X Female": {
									"caption": "Class-X Female",
									"type": "number"
								},
								"Class-XI Male": {
									"caption": "Class-XI Male",
									"type": "number"
								},
								"Class-XI Female": {
									"caption": "Class-XI Female",
									"type": "number"
								},
								"Class-XII Male": {
									"caption": "Class-XII Male",
									"type": "number"
								},
								"Class-XII Female": {
									"caption": "Class-XII Female",
									"type": "number"
								}
							}
						},
						"slice": {
							"reportFilters": [
								{
									"uniqueName": "District"
								}
							],
							"rows": [
								{
									"uniqueName": "Level"
								}
							],
							"columns": [
								{
									"uniqueName": "Location"
								},
								{
									"uniqueName": "Gender"
								}/* ,
								{
									"uniqueName": "Measures"
								} */
							],
							"measures": [
								{
									"uniqueName": "SEMIS Code",
									"aggregation": "count"
								}
							]
						}
					}
				});
				console.log("table", pivot);

			}
		}
	});

	function customizeToolbar(toolbar) {
		var tabs = toolbar.getTabs(); // get all tabs from the toolbar
		toolbar.getTabs = function () {
			delete tabs[0]; // delete the first tab
			delete tabs[1]; // delete the first tab
			delete tabs[2]; // delete the first tab
			return tabs;
		}
	}
}