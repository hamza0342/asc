# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ASCImagesKeyIndicator(Document):
	def validate(self):
		frappe.enqueue(self.check_data())
	def check_data(self):
		temp_query = "Select COUNT(name) AS schools from tabSchool where enabled = 1"
		data = frappe.db.sql(temp_query, as_dict = 1)
		self.total_schools = data[0]['schools']
		images_query = """Select COUNT( name) AS images , COUNT( CASE WHEN  source = 'Web' THEN semis_code ELSE NULL END) AS web, COUNT(DISTINCT CASE WHEN  source = 'Mobile' THEN semis_code ELSE NULL END) AS mobile, SUM(total_images) as total_images from `tabASC Images` where year = '%s' and docstatus!=2 """%(self.year)
		data_ = frappe.db.sql(images_query, as_dict=1)
		self.total_created =  data_[0]['images']
		self.remaining = data[0]['schools'] - data_[0]['images']
		self.total_web = data_[0]['web']
		self.total_mobile = data_[0]['mobile']
		self.total_images = data_[0]['total_images']
		# image_data_query = """SELECT s.district as district,count(DISTINCT s.name) as school, COUNT(DISTINCT CASE WHEN year = '%s' THEN i.semis_code ELSE NULL END) as total_images,
        # COUNT(DISTINCT CASE WHEN year = '%s' and i.source = 'Web' THEN i.semis_code ELSE NULL END) as web,
        # COUNT(DISTINCT CASE WHEN year = '%s' and i.source = 'Mobile' THEN i.semis_code ELSE NULL END) as mobile,
        # ( ( COUNT(DISTINCT s.name) ) - ( COUNT(DISTINCT CASE WHEN year = '%s' THEN i.semis_code ELSE NULL END)) ) as rem
        # , IFNULL(SUM(i.total_images),0) as uploaded_images
        # FROM tabSchool s
        # left join `tabASC Images` i
        # ON s.name=i.semis_code where s.enabled = '1'
        # GROUP BY s.district
        # ORDER BY s.district""" %(self.year,self.year,self.year,self.year)
		# table_data = frappe.db.sql(image_data_query,as_dict=1)
		# self.images_data = []
		# for r in table_data:
		# 	row = self.append('images_data',{})
		# 	row.district = r['district']
		# 	row.schools =  r['school']
		# 	row.total_asc_images = r['total_images']
		# 	row.remaining = r['rem']
		# 	row.web = r['web']
		# 	row.mobile = r['mobile']
		# 	row.uploaded_images = r['uploaded_images']
		districts = frappe.db.sql("Select district AS d from tabSchool group by district order by district")

 
		# for d in districts:
		# 	temp_query = """SELECT s.district as district,count(DISTINCT s.name) as school, COUNT( CASE WHEN year = '%s' THEN i.semis_code ELSE NULL END) as total_images,
		# 	COUNT(DISTINCT CASE WHEN year = '%s' and i.source = 'Web' THEN i.semis_code ELSE NULL END) as web,
		# 	COUNT(DISTINCT CASE WHEN year = '%s' and i.source = 'Mobile' THEN i.semis_code ELSE NULL END) as mobile,
		# 	( ( COUNT(DISTINCT s.name) ) - ( COUNT(DISTINCT CASE WHEN year = '%s' THEN i.semis_code ELSE NULL END)) ) as rem
		# 	, IFNULL(SUM(i.total_images),0) as uploaded_images
		# 	FROM tabSchool s
		# 	left join `tabASC Images` i
		# 	ON s.name=i.semis_code where s.enabled = '1' and s.district = '%s'
		# 	""" %(self.year,self.year,self.year,self.year,d[0])
		# 	r = frappe.db.sql(temp_query,as_dict=1)[0]
		# 	row = self.append('images_data',{})
		# 	row.district = r['district']
		# 	row.schools =  r['school']
		# 	row.total_asc_images = r['total_images']
		# 	row.remaining = r['rem']
		# 	row.web = r['web']
		# 	row.mobile = r['mobile']
		# 	row.uploaded_images = r['uploaded_images']
		self.images_data=[]
		for d in districts:
			data1=frappe.db.sql("SELECT s.district as district,count(DISTINCT s.name) as school FROM tabSchool s where s.enabled = '1' and s.district = '%s'"%(d[0]),as_dict = 1)[0]
			# frappe.msgprint(frappe.as_json(data1))
			row = self.append('images_data',{})
			row.district = data1['district']
			row.schools =  data1['school']
			query2 = """SELECT  COUNT(  i.semis_code ) as total_images
			FROM `tabASC Images` i where i.district = '%s' and year = '%s'
			""" %(d[0],self.year)
			data2=frappe.db.sql(query2,as_dict=1)[0]
			row.total_asc_images = data2['total_images']
			row.remaining = data1['school'] - data2['total_images']
			query3 = """SELECT  COUNT(DISTINCT CASE WHEN  i.source = 'Web' THEN i.semis_code ELSE NULL END) as web,
			COUNT(DISTINCT CASE WHEN  i.source = 'Mobile' THEN i.semis_code ELSE NULL END) as mobile,
			IFNULL(SUM(i.total_images),0) as uploaded_images
			FROM `tabASC Images` i where i.district = '%s' and year = '%s'
			""" %(d[0],self.year)
			data3=frappe.db.sql(query3,as_dict=1)[0]
			row.web = data3['web']
			row.mobile = data3['mobile']
			row.uploaded_images = data3['uploaded_images']