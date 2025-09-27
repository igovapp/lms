# Copyright (c) 2023, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from lms.lms.utils import has_course_instructor_role, has_course_moderator_role


class LMSQuestion(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from lms.lms.doctype.lms_question_option.lms_question_option import LMSQuestionOption

        multiple: DF.Check
        options: DF.Table[LMSQuestionOption]
        possibility_1: DF.SmallText | None
        possibility_2: DF.SmallText | None
        possibility_3: DF.SmallText | None
        possibility_4: DF.SmallText | None
        question: DF.TextEditor | None
        type: DF.Literal["Choices", "User Input", "Open Ended"]
    # end: auto-generated types

    def validate(self):
        validate_correct_answers(self)
        update_question_title(self)


def validate_correct_answers(question):
    if question.type == "Choices":
        validate_duplicate_options(question)
        validate_minimum_options(question)
        validate_correct_options(question)
    elif question.type == "User Input":
        validate_possible_answer(question)


def validate_duplicate_options(question : LMSQuestion):
    options = []

    for option in question.options :
        if option.get("option") :
            options.append(option.get(f"option"))

            pass
        pass

    if len(set(options)) != len(options):
        frappe.throw(_("Duplicate options found for this question."))


def validate_correct_options(question):
    correct_options = get_correct_options(question)

    if len(correct_options) > 1:
        question.multiple = 1

    if not len(correct_options):
        frappe.throw(_("At least one option must be correct for this question."))


def validate_minimum_options(question : LMSQuestion):
    if question.type == "Choices" and len(question.options) < 2:
        frappe.throw(_("Minimum two options are required for multiple choice questions."))


def validate_possible_answer(question):
    possible_answers = []
    possible_answers_fields = [
        "possibility_1",
        "possibility_2",
        "possibility_3",
        "possibility_4",
    ]

    for field in possible_answers_fields:
        if question.get(field):
            possible_answers.append(field)

    if not len(possible_answers):
        frappe.throw(
            _("Add at least one possible answer for this question: {0}").format(
                frappe.bold(question.question)
            )
        )


def update_question_title(question):
    if not question.is_new():
        question_rows = frappe.get_all("LMS Quiz Question", {"question": question.name}, pluck="name")

        for row in question_rows:
            frappe.db.set_value("LMS Quiz Question", row, "question_detail", question.question)


def get_correct_options(question : LMSQuestion):
    correct_options = []

    for option in question.options :
        if (option.get('is_correct')) == 1 :
            correct_options.append(option)

    return correct_options


@frappe.whitelist()
def get_question_details(question):
    if not has_course_instructor_role() or not has_course_moderator_role():
        return

    fields = ["question", "type", "name","options"]
    for i in range(1, 5):
        fields.append(f"explanation_{i}")
        fields.append(f"possibility_{i}")

    return frappe.db.get_value("LMS Question", question, fields, as_dict=1)
