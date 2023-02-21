# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os

class ASCImages(Document):
	def before_insert(self):
		if self.semis_code:
			check_enabled = frappe.db.get_value("School", self.semis_code, "enabled")
			if not check_enabled:
				frappe.throw("Invalid SEMIS Code")
		self.check_dublicate()
		if self.year is None:
			self.year = frappe.db.get_single_value("ASC Panel", "default_year")
	def validate(self):
		self.check_coordinates()
		self.count_total()
	def on_trash(self):
		pass
		'''if self.enabled == 0:
			import requests
			get_images = [self.image_1, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6, self.image_7, self.image_8]
			for x in get_images:
				if x:
					main_path = "https://semis.rsu-sindh.gov.pk" + str(x)
					img_data = requests.get(str(main_path)).content
					main_path_sch = "/home/xperterp/frappe-rsu/Downloads/disabled_imges/" + str(self.semis_code) + "/files"
					if not os.path.exists(main_path_sch):
						os.makedirs(main_path_sch)
					with open('/home/xperterp/frappe-rsu/Downloads/disabled_imges/' + str(self.semis_code) + str(x), 'wb') as handler:
	    					handler.write(img_data)
			if self.image_1:
				self.total_images += 1
			if self.image_2:
				self.total_images += 1
			if self.image_3:
				self.total_images += 1
			if self.image_4:
				self.total_images += 1
			if self.image_5:
				self.total_images += 1
			if self.image_6:
				self.total_images += 1
			if self.image_7:
				self.total_images += 1
			if self.image_8:
				self.total_images += 1'''
	def count_total(self):
		self.total_images = 0
		if self.image_1:
			self.total_images += 1
		if self.image_2:
			self.total_images += 1
		if self.image_3:
			self.total_images += 1
		if self.image_4:
			self.total_images += 1
		if self.image_5:
			self.total_images += 1
		if self.image_6:
			self.total_images += 1
		if self.image_7:
			self.total_images += 1
		if self.image_8:
			self.total_images += 1
	def check_dublicate(self):
		if frappe.db.exists("ASC Images", [["semis_code", "=", self.semis_code], ["year", "=", self.year]]):
			frappe.throw("This School Already Exists if you want to change please contact your LSU")
	def check_coordinates(self):
		if float(self.lat) < 24.0 or float(self.lat) > 30.0:
			frappe.throw("Lat Must be between 24 to 30")
		if float(self.lng) < 66.0 or float(self.lng) > 72.0:
			frappe.throw("lng Must be between 66 to 72") 
