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


# def readmission_limit(value):
#     """determine if field value exists in catalog index"""
#     catalog = api.portal.get_tool('portal_catalog')
#     results = catalog.searchResults(emplID=(value))
#     if results != -1:
#         raise Invalid(
#             _(u'Application on file. Please contact OSAS (osas@york.cuny.edu) for further help')
#             )
#     return True

# def email_constraint(value):
#     """Email validator"""
#     if '.' not in value and '@' not in value:
#         raise Invalid(_(u"Sorry, you've entered an invalid email address"))
#     return True


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

    Title = schema.TextLine(
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
        # constraint=
    )

    petitionType = schema.Choice(
        title=(u'Petition For: '),
        values=[(u'Grade Appeal')],
    )


    email = schema.TextLine(
        title=(u'Email Address'),
        required=True,
        # constraint=email_constraint,
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
        max_length=9,
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

    studentStatement = field.NamedBlobFile(
        title=(u'Personal Statement'),
        required=True,
    )

    supportingDocument = field.NamedBlobFile(
        title=(u'Supporting Document'),
        description=(u'Upload any supporting documentation here'),
        required=False,
    )
