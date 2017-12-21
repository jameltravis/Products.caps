# -*- coding: utf-8 -*-
"""CAPS Readmission form."""

from Products.caps import _
from zope import schema
from zope.interface import Invalid
from plone import api
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
            _(u'We have your application on file. Please contact OSAS (osas@york.cuny.edu) for further help')
            )
    return True

def email_contraint(value):
    """Email validator"""
    if '.' not in value and '@' not in value:
        raise Invalid(_(u"Sorry, you've entered an invalid email address"))
    return True


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


class IReadmission(model.Schema):
    """Class to create CAPS Readmission petition"""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
    )

    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        contstraint=email_contraint,
    )

    readmissionEmplID = schema.TextLine(
        title=(u'Empl ID'),
        description=(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min_length=8,
        max_length=8,
        constraint=readmission_limit,
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
        title=(u'For what semester '),
        value_type=DictRow(title=(u'Semester and Year'), schema=ISemester),
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
