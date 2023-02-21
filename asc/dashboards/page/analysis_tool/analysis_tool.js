frappe.pages['analysis-tool'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Analysis Tool',
		single_column: true
	});
	$(frappe.render_template("analysis_tool")).appendTo(page.main);

	var pivot = new Flexmonster({
		container: "#pivot-container",
		componentFolder: "https://cdn.flexmonster.com/",
		width: "100%",
		height: 430,
		toolbar: true,
		beforetoolbarcreated: customizeToolbar,
		report: {
			"dataSource": {
				"type": "api",
				"url": "https://semis.rsu-sindh.gov.pk:3400/api/cube",
				"index": "asc-kpi-2021"
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
					},
					{
						"uniqueName": "Measures"
					}
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
	function customizeToolbar(toolbar) {
		var tabs = toolbar.getTabs(); // get all tabs from the toolbar
		toolbar.getTabs = function () {
			delete tabs[0]; // delete the first tab
			delete tabs[1]; // delete the first tab
			delete tabs[2]; // delete the first tab
			return tabs;
		}
	}
	/*
	frappe.call({
		method: "asc.dashboards.page.analysis_tool.analysis_tool.get_data",
		freeze: true,
		callback: function (r) {
			//console.log(r.message);
			$(frappe.render_template("analysis_tool")).appendTo(page.main, { 'response': r.message });
				//alert('hello');
			
			
			
		},
	})*/

}
