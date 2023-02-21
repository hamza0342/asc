# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests as r

class UpdateDataByDate(Document):
	def validate(self):
		if self.date:
			get_data = r.get("http://semisrsu.com/index.php/SurveyAPI/get_schools_by_entry_date?date="
			+str(self.date)+"&token=c5e201884eebfc983819197b1e229ec6").json()
			self.school_info = []
			self.school_info = str({ "schoolinfo" : get_data["schoolInfo"]})
			self.teachers = []
			self.teachers = str({"teachers": get_data["teachers"]})
			self.enrollment = []
			self.enrollment = str({"enrollment" :get_data["enrollment"]})
			self.campus = []
			self.campus = str({"campus":get_data["campus"]})
			self.facilities = []
			self.facilities = str({"facilities":get_data["facilities"]})
			self.surrounding = []
			self.surrounding = str({"surrounding":get_data["surrounding"]})
