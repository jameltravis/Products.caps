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


class ISemester(model.Schema):
    """Used for semester and year schema"""

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


class IGradeAppeal(model.Schema):
    """Class to create Grade Appeal schema"""

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
        title=(u'For what semester'),
        value_type=DictRow(title=(u'Semester and Year'), schema=ISemester),
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
        required=True,
    )

    supportingDocument = field.NamedFile(
        title=(u'Supporting Document'),
        description=(u'Upload any supporting documentation here'),
        required=False,
    )
