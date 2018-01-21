# -*- coding: utf-8 -*-
"""Module for CAPS Grade change form."""

from Products.caps import _
# from Products.caps.validators import choice_constraint
from Products.caps.validators import name_check_constraint
from Products.caps.validators import email_constraint
from Products.caps.interfaces import ICourses
from Products.caps.interfaces import ISemester
from zope import schema
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


class IExtraCredits(model.Schema):
    """Class to create CAPS Leave of Absence Petition"""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
        constraint=name_check_constraint
    )

    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        contraint=email_constraint,
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
        max_length=10,
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
