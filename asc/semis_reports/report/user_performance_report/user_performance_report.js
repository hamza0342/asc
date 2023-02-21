// Copyright (c) 2016, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
let district_by_user;
let read_only = false;
frappe.query_reports["User Performance Report"] = {
	"filters": [
		{
			"fieldname":"district",
			"label": __("District"),
			"fieldtype": "Link",
			"options": "District",
			"default":`${district_by_user}`
		}
	],
	onload:async function() {
		var system_manager = frappe.user_roles.includes('System Manager');
		if (system_manager == false) {
			console.log("if log");
			await frappe.call({
				method: "frappe.dirp.report.user_performance_report.user_performance_report.district_by_user",
				args: { user: frappe.session.user },
				freeze:true,
				callback: function (r) {
					district_by_user = r.message.for_value;
					var dictrict_filter = frappe.query_report.get_filter('district');
					dictrict_filter.df.default = district_by_user;
					dictrict_filter.refresh();
					dictrict_filter.set_input(dictrict_filter.df.default);
					$("input[data-fieldname='district']").attr('readonly', true);

				}
			});
		} else {
			district_by_user = '';
			var dictrict_filter = frappe.query_report.get_filter('district');
			dictrict_filter.df.default = district_by_user;
			dictrict_filter.refresh();
			dictrict_filter.set_input(dictrict_filter.df.default);
		}
},
};
