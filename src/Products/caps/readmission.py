# -*- coding: utf-8 -*-
"""CAPS Readmission form.

The structure of the file from top to bottom is Validator functions,
Datagridfield classes, and Content type Schema.
"""

from Products.caps import _
from Products.caps.validators import readmission_limit_constraint
from Products.caps.validators import choice_constraint
from Products.caps.validators import name_check_constraint
from Products.caps.validators import email_constraint
from Products.caps.interfaces import ISemester
from Products.caps.interfaces import IPhoneNumbers
from plone.supermodel import model
from plone.directives import form
from plone.namedfile import field
from zope import schema
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


class IReadmission(model.Schema):
    """Used to create CAPS Readmission petition."""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last name'),
        required=True,
        constraint=name_check_constraint,
    )

    petitionType = schema.Choice(
        title=(u'Petition For: '),
        values=[
            (u'Select One'),
            (u'Readmission'),
            (u'Appeal of Dissmisal'),
            ],
        constraint=choice_constraint,
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
        constraint=readmission_limit_constraint,
    )

    # Data grid for Phone Numbers
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
