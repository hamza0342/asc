frappe.ui.form.on('Enrolment Class and Gender wise', {
    refresh: function(frm) {
      var full_class = frm.doc.boys + frm.doc.girls
      frm.set_value('total_class', full_class);
    }        
  });

