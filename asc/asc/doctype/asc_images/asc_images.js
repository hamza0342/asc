// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('ASC Images', {
	refresh: function (frm) {
		frappe.call({
			method: "asc.asc.doctype.asc.asc.get_defaults",
			callback: function (r) {
				if (frm.is_new()) {
					frm.set_value("year", r.message[1])
				}
			}
		});
	},
	onload: function (frm) {
		frappe.call({
			method: "asc.asc.doctype.asc.asc.get_defaults",
			callback: function (r) {
				if (frm.is_new()) {
					frm.set_value("year", r.message[1])
				}
			}
		});
	},
	lat: function (frm) {
		//if (!Number.isInteger(frm.doc.lat)){
		//	frm.set_value("lat",'')
		//}
		if (parseFloat(frm.doc.lat) < 24.0 || parseFloat(frm.doc.lat) > 30.0) {
			frm.set_value("lat", '')
			frappe.msgprint("Lat Must be between 24 to 30")
		}
	},
	lng: function (frm) {
		//if (!Number.isInteger(frm.doc.lng)){
		//	frm.set_value("lng",'')
		//}
		if (parseFloat(frm.doc.lng) < 66.0 || parseFloat(frm.doc.lng) > 72.0) {
			frm.set_value("lng", '')
			frappe.msgprint("lng Must be between 66 to 72")
		}
	}
});
