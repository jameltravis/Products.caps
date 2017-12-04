# -*- coding: utf-8 -*-
"""Module for CAPS Grade change form."""

from Products.caps import _
from zope import schema
# from zope import interface
# from zope.interface import Interface
# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


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

class IPhoneNumbers(model.Schema):
    """Class for Phone number datagrid"""

    cellPhoneNumber = schema.TextLine(
        title=(u'Phone Number (Cell)'),
        required=False,
    )

    homePhoneNumber = schema.TextLine(
        title=(u'Phone Number (Home)'),
        required=False,
    )


class ILeaveAbs(model.Schema):
    """Class to create CAPS General Petition"""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
    )

    petitionReason = schema.Choice(
        title=(u'Reason for Peition'),
        values=[
            (u"Extension INC"),
            (u"Grade Appeal"),
            (u"Grade Change"),
            (u"Other")
            ],
        required=True,
    )

    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        # contraint=email_constraint,
    )

    emplID = schema.Int(
        title=(u'Empl ID'),
        description=(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min=8,
        max=10,
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

    zipCode = schema.Int(
        title=(u'Zip Code'),
        description=(u'Enter your 5 digit zip code'),
        required=True,
        min=5,
        max=5
    )

    birthday = schema.Date(
        title=(u'Date of Birth'),
        required=True
    )

    # Data grid for semester and year
    form.widget(semesterInfo=DataGridFieldFactory)
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

    courseNumSection = schema.TextLine(
        title=_(u'Course Number and Section'),
        description=(u'Ex: CHEM 101'),
        required=True,
    )

    professor = schema.TextLine(
        title=(u'Course Instructor'),
        description=(u'Instructor of the afforementioned course'),
        required=True,
    )

    studentStatement = field.NamedFile(
        title=(u'Personal Statement'),
        description=(u'Be sure to include your last date of attendence for each course'),
        required=True,
    )

    supportingDocument = field.NamedFile(
        title=(u'Supporting Documentation'),
        description=(u'Upload any supporting documentation here'),
        required=False,
    )

    additionalDocuments = field.NamedFile(
        title=(u'Additional Documentation'),
        description=(u'If you have any additional documentation, upload it here'),
        required=False,
    )
