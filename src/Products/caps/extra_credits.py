# -*- coding: utf-8 -*-
"""Module for CAPS Grade change form."""

from Products.caps import _
from zope import schema
from zope import interface
# from zope.interface import Invalids
# from zope.interface import Interface
# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from plone.autoform import directives
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory

# Constraints
def email_constraint(value):
    """Email validator"""
    if '.' not in value and '@' not in value:
        raise interface.Invalid(_(u"Sorry, you've entered an invalid email address"))
    return True

def choice_constraint(value):
    """if the selection is left on default value, raise error message"""
    if value == (u'Select One'):
        raise interface.Invalid(_(u"Please select a choice"))
    else:
        return True


# Datagrid schema for the semesters
class ICourses(model.Schema):
    """Class for 'Course' DataGrid schema"""

    course = schema.TextLine(
        title=(u'Course and Course Number'),
        description=(u'Ex: CHEM 101'),
    )

    courseCode = schema.TextLine(
        title=(u'Code'),
        description=(u'Ex: 12345'),
        max_length=5,
    )

    courseSection = schema.TextLine(
        title=(u'Section'),
        description=(u'Ex: YY'),
    )

# Datagrid schema for selecting the semester year
class ISemester(model.Schema):
    """Used for semester and year DataGrid schema"""

    semester = schema.Choice(
        title=(u'Semester'),
        values=[
            (u'Fall'),
            (u'Winter'),
            (u'Spring'),
            (u'Summer'),
        ],
        required=True,
    )

    semesterYear = schema.TextLine(
        title=(u'Year'),
        required=True,
    )


class IExtraCredits(model.Schema):
    """Class to create CAPS Petition for Excess Credits"""

    title = schema.TextLine(
        title=(u'First Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
    )

    # LastName = schema.TextLine(
    #     title=(u'Last Name'),
    #     description=(u'Please enter your Last Name'),
    #     required=True,
    # )

    petitionType = schema.Choice(
        title=(u'Petition For: '),
        values=[(u'Extra Credits')],
    )

    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        constraint=email_constraint,
    )

    emplID = schema.TextLine(
        title=(u'Empl ID'),
        description=(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min_length=8,
        max_length=8,
    )

    cellPhoneNumber = schema.TextLine(
        title=(u'Phone Number (Cell)'),
        required=False,
    )

    homePhoneNumber = schema.TextLine(
        title=(u'Phone Number (Home)'),
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
        max_length=5,
    )

    birthday = schema.Date(
        title=(u'Date of Birth'),
        required=True
    )

    # Data grid for semester and year
    form.widget(semesterInfo=DataGridFieldFactory)
    # form.widget['semesterInfo'].allow_insert = False
    semesterInfo = schema.List(
        title=(u'Semester'),
        value_type=DictRow(title=(u'Semester and Year'), schema=ISemester),
        required=False,
    )

    form.widget(coursesDropped=DataGridFieldFactory)
    coursesDropped = schema.List(
        title=(u'Courses'),
        value_type=DictRow(title=(u'Courses to be withdrawn from'), schema=ICourses),
        required=False,
    )

    studentStatement = field.NamedBlobFile(
        title=(u'Personal Statement'),
        description=(u'Be sure to include your last date of attendence for each course'),
        required=True,
    )

    supportingDocument = field.NamedBlobFile(
        title=(u'Supporting Documentation'),
        description=(u'Upload any supporting documentation here'),
        required=False,
    )

    additionalDocuments = field.NamedBlobFile(
        title=(u'Additional Documentation'),
        description=(u'If you have any additional documentation, upload it here'),
        required=False,
    )
