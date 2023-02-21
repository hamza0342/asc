frappe.pages['facilities-map'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Facilities Map',
		single_column: true,

	});
	console.log("Route Data", frappe.get_route());
	$(".select-icon").css('top: 7px');

	filters.add(page);
	// $("input[data-fieldname='basic_facility']").css('align-items: center;');
	$(".select-icon").css('top: 7px');

	// $(".frappe-control[data-fieldtype='Select'], .form-group, .select-icon.xs").css('top: 7px');
	var basic_facility = "Drinking Water"
	var year = "2021-22"

	if (frappe.get_route().length > 1) {
		if (frappe.get_route()[1]) {
			year = frappe.get_route()[1]
		}
		if (frappe.get_route()[2]) {
			basic_facility = frappe.get_route()[2]
		}
	}

	frappe.call({
		method: "asc.dashboards.page.facilities_map.facilities_map.get_data",
		freeze: true,
		args: {
			basic_facility: basic_facility,
			year: year,
			freeze: true,
		},

		callback: function (r) {
			// console.log("Callback");
			//console.log(r.message);
			// console.log("Callback end");
			var data = r.message[0];

			$('#mainBody').remove();


			$(
				frappe.render_template("facilities_map", { 'type': basic_facility })
			).appendTo(page.main);
			$("#profile_items").hide()
			$("#barContainer").hide()


			draw_map(r.message[0], r.message[1], basic_facility, year, page);
			legend = true


			barChart2(r.message[0], basic_facility, 'barContainer2', legend, 'bar')

			//provinceChart2(data, r.message[1], basic_facility.get_value());
		},
	});

}

filters = {
	add: function (page) {
		var basic_facility_ = "Drinking Water"
		var year_ = "2021-22"

		if (frappe.get_route().length > 1) {
			if (frappe.get_route()[1]) {
				year_ = frappe.get_route()[1]
			}
			if (frappe.get_route()[2]) {
				basic_facility_ = frappe.get_route()[2]
			}
		}
		let year = page.add_field({
			label: "Year",
			fieldtype: "Link",
			fieldname: "Year",
			options: "Year",
			default: year_,
			reqd: 1,
		});
		let division = page.add_field({
			label: "Division",
			fieldtype: "Link",
			fieldname: "division",
			options: "Division",
		});
		let basic_facility = page.add_field({
			label: "Basic Facility",
			fieldtype: "Select",
			fieldname: "basic_facility",
			default: basic_facility_,
			options: ["", "Drinking Water", "Electricity", "Building", "Boundary Wall", "Toilet", "Hand Wash", "Soap", "MHM Disposal"],
			reqd: 1,
		});
		let fiterbtn = page.add_field({
			label: "View",
			fieldtype: "Button",
			fieldname: "filter",
			click() {
				if (basic_facility.get_value() == "" || year.get_value() == "") {
					if (year.get_value() == "" && basic_facility.get_value() == "") {
						frappe.msgprint("Please Select Year and Facility");
						return;
					}
					if (year.get_value() == "") {
						frappe.msgprint("Please Select Year");
						return;
					}
					if (basic_facility.get_value() == "") {
						frappe.msgprint("Please Select Facility");
						return;
					}

				} else {
					//console.log("Inside Click");


					frappe.call({
						method: "asc.dashboards.page.facilities_map.facilities_map.get_data",
						freeze: true,
						args: {
							basic_facility: basic_facility.get_value(),
							year: year.get_value(),
							division: division.get_value(),
							freeze: true,
						},

						callback: function (r) {
							// console.log("Callback");
							//console.log(r.message);
							// console.log("Callback end");
							var data = r.message[0];

							$('#mainBody').remove();


							$(
								frappe.render_template("facilities_map", { 'type': basic_facility.get_value() })
							).appendTo(page.main);
							$("#profile_items").hide()
							$("#barContainer").hide()


							draw_map(r.message[0], r.message[1], basic_facility.get_value(), year.get_value(), page);
							legend = true
							if (division.get_value() != "") {
								legend = true
							}

							barChart2(r.message[0], basic_facility.get_value(), 'barContainer2', legend, 'bar')

							//provinceChart2(data, r.message[1], basic_facility.get_value());
						},
					});
				}
			},
		});






	},
};//end of filters

function barChart(data_, facility_name, container, legend, type, height) {
	categoery = []
	facility_available = []
	facility_not_available = []
	for (let i = 0; i < data_.length; i++) {
		categoery[i] = data_[i].name;
		facility_available[i] = data_[i].value;
		facility_not_available[i] = parseFloat((100 - data_[i].value).toFixed(1));
	}
	console.log(facility_available);
	console.log(facility_not_available);

	Highcharts.chart(container, {
		chart: {
			type: type,
			height: 350,
			// width: 450,
		},
		credits: {
			enabled: false,
		},
		title: {
			text: facility_name + ' Facility',
			align: 'left',
			style: {
				fontWeight: 'bold',
				fontSize: '16px',
			}
		},
		xAxis: {
			categories: categoery,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: ""
			}
		},
		legend: {
			reversed: true,
			enabled: legend,
		},

		plotOptions: {
			series: {
				pointWidth: 28,
				stacking: 'percent',
				dataLabels: {
					enabled: true,
					formatter: function () {
						if (this.y) {
							return this.y;
						}
					},
					position: "left",
					allowOverlap: true,
					crop: false,
					padding: 0,

				},
			}
		},
		series: [{
			name: 'Schools with ' + facility_name,
			data: facility_available,
			color: '#345C0C',
		}, {
			name: 'Other Schools',
			data: facility_not_available,
			color: '#EAB10B',


		}]
	});


}
function barChart2(data_, facility_name, container, legend, type, height) {
	categoery = []
	facility_available = []
	facility_not_available = []
	for (let i = 0; i < data_.length; i++) {
		categoery[i] = data_[i].name;
		facility_available[i] = data_[i].value;
		facility_not_available[i] = parseFloat((100 - data_[i].value).toFixed(1));
	}
	console.log(facility_available);
	console.log(facility_not_available);

	Highcharts.chart(container, {
		chart: {
			type: type,
			// width: 450,
		},
		credits: {
			enabled: false,
		},
		title: {
			text: facility_name + ' Facility',
			align: 'left',
			style: {
				fontWeight: 'bold',
				fontSize: '16px',
			}
		},
		xAxis: {
			categories: categoery,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: ""
			}
		},
		legend: {
			reversed: true,
			enabled: legend,
		},

		plotOptions: {
			series: {
				pointWidth: 28,
				stacking: 'percent',
				dataLabels: {
					enabled: true,
					formatter: function () {
						if (this.y) {
							return this.y;
						}
					},
					position: "left",
					allowOverlap: true,
					crop: false,
					padding: 0,

				},
			}
		},
		series: [{
			name: 'Schools with ' + facility_name,
			data: facility_available,
			color: '#345C0C',
		}, {
			name: 'Other Schools',
			data: facility_not_available,
			color: '#EAB10B',


		}]
	});


}




function draw_map(adata, color, facility, year, page) {
	var series = [{
		type: 'map',
		enableMouseTracking: true,
		showInLegend: false,
		animation: {
			duration: 1000
		},
		data: adata,
		dataLabels: {
			enabled: true,
			color: '#FFFFFF',
			format: '{point.name} <br />( {point.value} %)'
		},
		name: facility + ' Availability',
		states: {
			hover: {
				borderColor: '#FFFFFF'
			}
		},
		tooltip: {
			pointFormat: 'District: {point.name} <br /> Total Schools: {point.Total_Schools}<br />Schools with ' + facility + ': {point.facility_available} ({point.value}%)<br /><br />'
		}
	}];
	Highcharts.mapChart('mapContainer', {
		title: {
			text: ''
		},
		mapNavigation: {
			enabled: true,
			buttonOptions: {
				alignTo: 'spacingBox',
				x: 10
			}
		},
		colorAxis: {
			dataClasses: color
		},
		legend: {
			layout: 'vertical',
			align: 'left',
			verticalAlign: 'bottom',
			floating: true,

		},
		plotOptions: {
			series: {
				events: {
					click: function (e) {
						frappe.call({
							method: "asc.dashboards.page.facilities_map.facilities_map.get_taluka_data",
							freeze: true,
							args: {
								basic_facility: facility,
								year: year,
								district: e.point.name,
								freeze: true,
							},

							callback: function (r) {
								console.log("Callback2");
								console.log(r.message);
								console.log("Callback 2 end");

								// $('#mainBody').remove();


								// $(
								// 	frappe.render_template("facilities_map", { 'type': facility })
								// ).appendTo(page.main);

								// draw_map(r.message.District, facility, year, page);
								$("#profile_items").show()
								$("#barContainer").show()
								$("#barContainer2").hide()
								$('[data-toggle="tooltip"]').tooltip();
								// console.log(r.message.District[0].name);
								$('#district_name').html(r.message.District[0].name)

								$('#school').html((r.message.District[0].total_schools).toLocaleString("en-US"))

								$('#functional').html((r.message.District[0].funcional).toLocaleString("en-US"))
								$('#closed').html((r.message.District[0].closed).toLocaleString("en-US"))

								$('#male_enrollment').html((r.message.District[0].male_enrollment).toLocaleString("en-US"))
								$('#female_enrollment').html((r.message.District[0].female_enrollment).toLocaleString("en-US"))
								$('#enrollment').html((r.message.District[0].male_enrollment + r.message.District[0].female_enrollment).toLocaleString("en-US"))


								$('#teachers').html((r.message.District[0].male_teachers + r.message.District[0].female_teachers).toLocaleString("en-US"))
								$('#male_teachers').html((r.message.District[0].male_teachers).toLocaleString("en-US"))
								$('#female_teachers').html((r.message.District[0].female_teachers).toLocaleString("en-US"))

								var data = String(r.message.District[0].primary.toLocaleString("en-US")) + " (" + String(r.message.District[0].primary_percentage) + "%)"
								$('#primary').html(data)

								var data = String(r.message.District[0].elementry.toLocaleString("en-US")) + " (" + String(r.message.District[0].elementry_percentage) + "%)"
								$('#elementary').html(data)

								var data = String(r.message.District[0].middle.toLocaleString("en-US")) + " (" + String(r.message.District[0].middle_percentage) + "%)"
								$('#middle').html(data)

								var data = String(r.message.District[0].secondary.toLocaleString("en-US")) + " (" + String(r.message.District[0].secondary_percentage) + "%)"
								$('#secondary').html(data)

								var data = String(r.message.District[0].higher_secondary.toLocaleString("en-US")) + " (" + String(r.message.District[0].higher_secondary_percentage) + "%)"
								$('#higher_secondary').html(data)


								$('#boys').html(r.message.District[0].boys.toLocaleString("en-US"))
								$('#girls').html(r.message.District[0].girls.toLocaleString("en-US"))
								$('#mixed').html(r.message.District[0].mixed.toLocaleString("en-US"))

								var data = String(r.message.District[0].hand_wash_percentage) + "%"
								$('#hand_wash_percentage').html(data);

								var data = String(r.message.District[0].boundary_wall_percentage) + "%"
								$('#boundary_wall_percentage').html(data)

								var data = String(r.message.District[0].water_percentage) + "%"
								$('#water_percentage').html(data);

								var data = String(r.message.District[0].mhm_percentage) + "%"
								$('#mhm_percentage').html(data)


								var data = String(r.message.District[0].building_percentage) + "%"
								$('#building_percentage').html(data)

								var data = String(r.message.District[0].toilet_percentage) + "%"
								$('#toilet_percentage').html(data)

								var data = String(r.message.District[0].electricity_percentage) + "%"
								$('#electricity_percentage').html(data)

								var data = String(r.message.District[0].soap_percentage) + "%"
								$('#soap_percentage').html(data)

								barChart(r.message.Taluka, facility, 'barContainer', false, 'column')
								$('#close_btn').click(function () {
									$("#profile_items").hide()
									$("#barContainer").hide()
									$("#barContainer2").show()
								});


							},
						});
					}
				}
			}
		},
		credits: {
			enabled: false,
		},
		exporting: {
			enabled: true
		},
		series: series
	});
}

