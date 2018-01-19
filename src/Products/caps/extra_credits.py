# -*- coding: utf-8 -*-
"""Module for CAPS Grade change form."""

from Products.caps import _
from Products.caps.validators import choice_constraint
from Products.caps.validators import name_check_constraint
from Products.caps.validators import email_constraint
from Products.caps.interfaces import ISemester
from Products.caps.interfaces import ICourses
from zope import schema
from plone.supermodel import model
from plone.namedfile import field
from plone.directives import form
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


class IExtraCredits(model.Schema):
    """Class to create CAPS Petition for Excess Credits"""

    title = schema.TextLine(
        title=(u'First and Last Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
        contraint=name_check_constraint,
    )

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
