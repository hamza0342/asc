frappe.pages['primary-to-post-prim'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Transition Rate',
		single_column: true,

	});
	$(".select-icon").css('top: 7px');
	filters.add(page);
	$(".select-icon").css('top: 7px');

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
		let gender = page.add_field({
			label: "Gender",
			fieldtype: "Select",
			fieldname: "gender",
			options: ["", "Boys", "Girls"],
		});
		let transition_type = page.add_field({
			label: "Transition",
			fieldtype: "Select",
			fieldname: "transition_type",
			options: ["", "Primary to Post Primary", "Middle to Secondary"],
			default: "Primary to Post Primary",
			reqd: 1,
		});
		let fiterbtn = page.add_field({
			label: "View",
			fieldtype: "Button",
			fieldname: "filter",
			click() {
				if (year.get_value() == "" || transition_type.get_value() == "") {
					frappe.msgprint("Year and Transition are Mandatory");
					return;
				} else {
					frappe.call({
						method: "asc.dashboards.page.primary_to_post_prim.primary_to_post_prim.get_data",
						freeze: true,
						args: {
							year: year.get_value(),
							division: division.get_value(),
							gender: gender.get_value(),
							transition_type: transition_type.get_value(),
							freeze: true,
						},

						callback: function (r) {
							// console.log("Callback");
							//console.log(r.message);
							// console.log("Callback end");
							var data = r.message[0];
							$('#mainBody').remove();


							$(frappe.render_template("primary_to_post_prim")).appendTo(page.main);

							draw_map(r.message[0], r.message[1], year.get_value(), page);
							legend = true
							if (division.get_value() != "") {
								legend = true
							}

							//provinceChart2(data, r.message[1], basic_facility.get_value());
						},
					});
				}
			},
		});






	},
};//end of filters

function draw_map(adata, pre_year, year, page) {
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
		name: ' Primary to Post-Primary',
		states: {
			hover: {
				borderColor: '#FFFFFF'
			}
		},
		tooltip: {
			pointFormat: 'District: {point.name} <br /> Primary to Post-Primary: ({point.value}%)<br /><br />'
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
			stops: [
				[0, '#ff0000'],
				[.7, '#13ef16'],
				[1, '#055406']
			]
		},
		legend: {
			layout: 'vertical',
			align: 'left',
			verticalAlign: 'bottom',
			floating: true,

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
