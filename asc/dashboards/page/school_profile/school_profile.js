frappe.pages['school-profile'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'School Profile',
		single_column: true
	});
}