# -*- coding: utf-8 -*-
"""CAPS Readmission form.

The structure of the file from top to bottom is Validator functions,
Datagridfield classes, and Content type Schema.
"""

from Products.caps import _
from Products.caps import validators
# from plone import api
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from zope import schema
# from zope import interface
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory

# def readmission_limit_constraint(value):
#     """determine if field value exists in catalog index."""
#     catalog = api.portal.get_tool('portal_catalog')
#     results = catalog.searchResults(**{'portal_type': 'Readmission', 'emplID': value})
#     if len(results) > 3:
#         raise interface.Invalid(
#             _(u'Application on file. Please contact OSAS (osas@york.cuny.edu) for further help')
#         )
#     else:
#         return True

# def name_check_constraint(value):
#     """ensures that student enters at least two words/names"""
#     if ' ' not in value:
#         raise interface.Invalid(_(u"Please enter your first AND last name"))
#     return True

# def email_constraint(value):
#     """Email validator"""
#     if '.' not in value and '@' not in value:
#         raise interface.Invalid(_(u"Sorry, you've entered an invalid email address"))
#     return True

# def choice_constraint(value):
#     """if the selection is left on default value, raise error message"""
#     if value == (u'Select One'):
#         raise interface.Invalid(_(u"Please select a choice"))
#     else:
#         return True


class ISemester(model.Schema):
    """Generates 'Semester' DataGridField."""

    semester = schema.Choice(
        title=(u'Semester'),
        values=[
            (u'Select One'),
            (u'Fall'),
            (u'Winter'),
            (u'Spring'),
            (u'Summer'),
        ],
        required=True,
        constraint=validators.choice_constraint,
    )

    semesterYear = schema.TextLine(
        title=(u'Year'),
        required=True,
    )

class IPhoneNumbers(model.Schema):
    """Used for Phone number datagrid"""

    cellPhoneNumber = schema.TextLine(
        title=(u'Phone Number (Cell)'),
        required=False,
    )

    homePhoneNumber = schema.TextLine(
        title=(u'Phone Number (Home)'),
        required=False,
    )


class IReadmission(model.Schema):
    """Used to create CAPS Readmission petition."""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last name'),
        required=True,
        constraint=validators.name_check_constraint,
    )

    petitionType = schema.Choice(
        title=(u'Petition For: '),
        values=[
            (u'Select One'),
            (u'Readmission'),
            (u'Appeal of Dissmisal'),
            ],
        constraint=validators.choice_constraint,
    )

    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        constraint=validators.email_constraint,
    )

    emplID = schema.TextLine(
        title=(u'Empl ID'),
        description=(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min_length=8,
        max_length=8,
        constraint=validators.readmission_limit_constraint,
    )

    # Data grid for semester and year
    form.widget(phoneNumbers=DataGridFieldFactory)
    phoneNumbers = schema.List(
        title=(u'Please enter your phone numbers'),
        value_type=DictRow(title=(u'Phone numbers'), schema=IPhoneNumbers),
        required=False,
    )

    address = schema.TextLine(
        title=(u'Address'),
        description=(u'Enter your home address, including apartment number'),
        required=True,
    )

    city = schema.TextLine(
        title=(u'City'),
        required=True,
    )

    zipCode = schema.TextLine(
        title=(u'Zip Code'),
        description=(u'Enter your 5 digit zip code'),
        required=True,
        min_length=5,
        max_length=10,
    )

    birthday = schema.Date(
        title=(u'Date of Birth'),
        required=True
    )

    # Data grid for semester and year
    form.widget(semesterInfo=DataGridFieldFactory)
    semesterInfo = schema.List(
        title=(u'For what semester are you seeking readmission?'),
        value_type=DictRow(title=(u'Semester and Year'), schema=ISemester),
        required=True,
    )

    studentStatement = field.NamedBlobFile(
        title=(u'Personal Statement'),
        description=(
            u'Address reasons for past academic difficulties, and detailed plan for change'
            ),
        required=True,
    )

    transcript = field.NamedBlobFile(
        title=(u'Transcript'),
        description=(u'Petitions without transcripts will not be considered'),
        required=True
    )

    supportingDocument = field.NamedBlobFile(
        title=(u'Supporting Document'),
        description=(u'Upload any supporting documentation here'),
        required=False,
    )

    additionalDocuments = field.NamedBlobFile(
        title=(u'Additional Documents'),
        description=(u'Upload additional supporting documentation here'),
        required=False,
    )
