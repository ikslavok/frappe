# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from frappe.website.doctype.personal_data_download_request.personal_data_download_request import get_user_data
from erpnext.shopping_cart.test_shopping_cart import create_user_if_not_exists

class TestRequestPersonalData(unittest.TestCase):
	def setUp(self):
		create_user_if_not_exists('test@example.com')
		frappe.set_user('test@example.com')

	def test_user_data(self):
		user_data = get_user_data('test@example.com')
		expected_data = {'Contact': frappe.get_all('Contact', {'email_id':'test@example.com'},["*"])}
		self.assertEqual(user_data, expected_data)

	def test_file_and_email_creation(self):
		download_request = frappe.get_doc({"doctype": 'Personal Data Download Request', 'user': 'test@example.com'})
		download_request.save()
		
		f = frappe.get_all('File', 
			{'attached_to_doctype':'Personal Data Download Request', 'attached_to_name': download_request.name}, 
			['*'])
		self.assertEqual(len(f), 1)

		email_queue = frappe.db.sql("""select * from `tabEmail Queue`""", as_dict=True)
		self.assertTrue("Subject: ERPNext: User Data" in email_queue[0].message)
		
		frappe.db.sql("delete from `tabEmail Queue`")