# Copyright (c) 2024, Farsi Ansari and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class LibraryMembership(Document):
	def before_submit(self): 
		exists = frappe.db.exists( "Library Membership", { 
			"library_member": self.library_member, 
			"docstatus": 1, # check for submitted documents 
			"to_date": (">", self.from_date), # check if the membership's end date is later than this membership's start date 
			}, 
		)
		if exists: 
			frappe.throw("There is an active membership for this member")

		loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
		self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
