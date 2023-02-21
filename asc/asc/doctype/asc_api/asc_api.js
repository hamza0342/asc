// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('ASC Api', {
	// refresh: function(frm) {
	import_data: function (frm) {
		frappe.call({
			method: "frappe.integrations.asc_doctype_api.get_asc_api",
			// method: "frappe.integrations.teachers_api.get_asc_api",
			args: {
				// date: frm.doc.main_date,
				// import_teachers: frm.doc.import_teachers

				//page: frm.doc.page
			},
			callback: function (r) {
				//console.group(r.message)
			}
		});
	}
	// }
});
