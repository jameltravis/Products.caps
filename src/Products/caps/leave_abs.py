# -*- coding: utf-8 -*-
"""Module for CAPS Grade change form."""

from Products.caps import _
from zope import schema
from zope.interface import Invalid
# from zope import interface
# from zope.interface import Interface
# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


def readmission_limit(value):
    """determine if field value exists in catalog index"""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog.searchResults(emplID=(value))
    if results != -1:
        raise Invalid(
            _(u'Application on file. Please contact OSAS (osas@york.cuny.edu) for further help')
            )
    return True

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


class IExtraCredits(model.Schema):
    """Class to create CAPS Leave of Absence Petition"""

    firstName = schema.TextLine(
        title=(u'First Name'),
        description=(u'Please enter your First Name'),
        required=True,
    )

    LastName = schema.TextLine(
        title=(u'First Name'),
        description=(u'Please enter your Last Name'),
        required=True,
    )

    petitionType = schema.Choice(
        title=(u'Petition For: '),
        values=[(u'Extra Credits')],
    )


    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        contraint=email_constraint,
    )

    emplID = schema.Int(
        title=(u'Empl ID'),
        description=(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min=10000000,
        max=99999999,
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

    zipCode = schema.Int(
        title=(u'Zip Code'),
        description=(u'Enter your 5 digit zip code'),
        required=True,
        min=501,
        max=99999,
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

    # Data grid for dropped courses
    form.widget(coursesDropped=DataGridFieldFactory)
    coursesDropped = schema.List(
        title=(u'Courses'),
        value_type=DictRow(title=(u'Courses to be withdrawn from'), schema=ICourses),
        required=False,
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