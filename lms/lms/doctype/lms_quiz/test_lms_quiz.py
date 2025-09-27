# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

# import frappe
import unittest

import frappe


class TestLMSQuiz(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        frappe.get_doc({"doctype": "LMS Quiz", "title": "Test Quiz", "passing_percentage": 90}).save(
            ignore_permissions=True
        )

    def test_with_multiple_options(self):
        question = frappe.new_doc("LMS Question")
        question.question = "Question Multiple"
        question.type = "Choices"
        question.append("options", {
            'option' : "Option 1",
            'is_correct' : 1
        })

        question.append("options", {
            'option' : "Option 2",
            'is_correct' : 1
        })

        question.save()
        self.assertTrue(question.multiple)

    def test_with_no_correct_option(self):
        question = frappe.new_doc("LMS Question")
        question.question = "Question Multiple"
        question.type = "Choices"

        question.append("options", {
            'option' : "Option 1",
            'is_correct' : 0
        })

        question.append("options", {
            'option' : "Option 2",
            'is_correct' : 0
        })

        self.assertRaises(frappe.ValidationError, question.save)

    def test_with_no_possible_answers(self):
        question = frappe.new_doc("LMS Question")
        question.question = "Question Multiple"
        question.type = "User Input"
        self.assertRaises(frappe.ValidationError, question.save)

    @classmethod
    def tearDownClass(cls) -> None:
        frappe.db.delete("LMS Quiz", "test-quiz")
        frappe.db.delete("LMS Question")
