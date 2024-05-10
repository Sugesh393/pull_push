# Copyright (c) 2024, Farsi Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ChildTableTask(Document):
	def before_save(self):
		ext = frappe.get_all("Child Record", {}, "*")
		for i in ext:
			self.append("existing", {
				"name1": i.ct_name,
				"date": i.ct_date
			})
		
		if(self.existing):
			# for i in self.insertion:
			# 	count = 1
			# 	for e in self.existing:
			# 		if (i.name1 == e.name1 and i.date == str(e.date)):
			# 			count = 0
			# 			break
			# 	if count:
			# 		self.append("common", {
			# 			"name1": i.name1,
			# 			"date": i.date
			# 		})
			res = frappe.db.sql(f""" SELECT t1.name1, t1.date 
					   FROM `tabInserting` t1 
					   WHERE NOT EXISTS (SELECT 1 FROM `tabExisting` t2 WHERE t1.name1 = t2.name1 and t1.date = t2.date 
					   and t2.parent = "{self.name}") and t1.parent = "{self.name}";  """, 
					   as_dict=1
			)
			for i in res:
				self.append("common", {
						"name1": i.name1,
						"date": i.date
				})

		else:
			for i in self.insertion:
				self.append("common", {
						"name1": i.name1,
						"date": i.date
				})


	def on_submit(self):
		for i in self.common:
			record = frappe.new_doc("Child Record")
			record.ct_name = i.name1
			record.ct_date = i.date
			record.insert()
