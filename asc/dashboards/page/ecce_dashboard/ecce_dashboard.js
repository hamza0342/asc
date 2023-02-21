frappe.pages['ecce-dashboard'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'ECCE Dashboard',
		single_column: true
	});
	filters.add(page);

}

filters = {
	add: function (page) {
		let year = page.add_field({
			label: "Year",
			fieldtype: "Link",
			fieldname: "Year",
			options: "Year",
			default: "2021-22",
			reqd: 1,
		});
		let division = page.add_field({
			label: "Division",
			fieldtype: "Link",
			fieldname: "division",
			options: "Division",
		});
		let basic_facility = page.add_field({
			label: "ECCE Detail",
			fieldtype: "Select",
			fieldname: "basic_facility",
			default: "ECCE Enrollment",
			options: ["", "ECCE Enrollment", "ECCE Rooms"],
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
						frappe.msgprint("Please Select ECCE Detail");
						return;
					}

				} else {
					console.log("Inside Click");


					frappe.call({
						method: "asc.dashboards.page.ecce_dashboard.ecce_dashboard.get_data",
						freeze: true,
						args: {
							basic_facility: basic_facility.get_value(),
							year: year.get_value(),
							division: division.get_value(),
							freeze: true,
						},

						callback: function (r) {
							console.log("Callback");
							console.log(r.message);
							console.log("Callback end");
							var data = r.message[0];

							$('#mainBody').remove();


							$(
								frappe.render_template("ecce_dashboard", { 'type': basic_facility.get_value() })
							).appendTo(page.main);

							draw_map(r.message, basic_facility.get_value());

							// barChart(r.message, basic_facility.get_value());
							drawStackedBar(r.message, basic_facility.get_value());


						},
					});
				}
			},
		});
	},
};//end of filters




function drawStackedBar(data_, facility_name) {
	facility_name = "Schools % with " + facility_name;
	categoery = []
	ecce_available = []
	ecce_not_available = []
	for (let i = 0; i < data_.length; i++) {
		categoery[i] = data_[i].name;
		ecce_available[i] = data_[i].value;
		ecce_not_available[i] = parseFloat((100 - data_[i].value).toFixed(1));
	}


	Highcharts.chart('barContainer', {
		chart: {
			type: 'bar'
		},
		credits: {
			enabled: false,
		},
		title: {
			text: facility_name
		},
		xAxis: {
			categories: categoery,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: facility_name
			}
		},
		legend: {
			reversed: true
		},

		plotOptions: {
			series: {
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
			name: facility_name,
			data: ecce_available,
			color: '#345C0C',
		}, {
			name: 'Other Schools',
			data: ecce_not_available,
			color: '#EAB10B',


		}]
	});

}

function draw_map(adata, facility) {
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
			pointFormat: 'District: {point.name} <br /> Total Schools: {point.Total_Schools}<br />Schools with ' + facility + ': {point.facility_available} ({point.value}%)<br />ECCE Enrollment {point.ecce_enrollment}<br />'
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
			dataClasses: [{
				from: 0,
				to: 5,
				color: '#F80000',
				name: 'Below 5%'
			}, {
				from: 5,
				to: 20,
				color: '#F7C10B',
				name: '5%-20%'
			}, {
				from: 20,
				to: 40,
				color: '#4a9957',
				name: '21%-40%'
			}, {
				from: 40,
				to: 100,
				color: '#345C0C',
				name: 'Above 40%'
			}]
		},
		legend: {
			layout: 'vertical',
			align: 'left',
			verticalAlign: 'bottom'
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