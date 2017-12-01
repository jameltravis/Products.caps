# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from zope import schema
from zope.interface import Interface
from plone.supermodel import model
from plone.schema import Email
from plone.namedfield import field
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from z3c.form import form


# def email_constraint(value):
#     """Email validation of string field"""

#     if "@" and "." not in value:
#         raise zope.interface.Invalid(u'Please enter a valid email address')
#     return True


class IPhoneNumbers(Interface):
    """Class for Phone number datagrid"""

    cellPhoneNumber = schema.TextLine(
        title=_(u'Phone Number (Cell)'),
        required=False,
    )

    homePhoneNumber = schema.TextLine(
        title=_(u'Phone Number (Home)'),
        required=False,
    )


class ISemester(Interface):
    """Used for semester and year schema"""

    semester = schema.Choice(
        title=_(u'Semester'),
        values=[
            _(u'Fall'),
            _(u'Winter'),
            _(u'Spring'),
            _(u'Summer'),
        ],
        required=True,
    )

    semesterYear = schema.TextLine(
        title=_(u'Year'),
        required=True,
    )


class IGenPetition(model.Schema):
    """Class to create CAPS General Petition"""

    lastName = schema.TextLine(
        title=_(u'Last Name'),
        description=_(u'Please enter your surname'),
        required=True,
    )

    firstName = schema.TextLine(
        title=_(u'First Name'),
        description=_(u'Please enter your given name'),
        required=True,
    )

    title = lastName.upper() + ", " + firstName.upper()

    petitionReason = schema.Choice(
        title=_(u'Reason for Peition'),
        values=[
            _(u"Extension INC"),
            _(u"Grade Appeal"),
            _(u"Grade Change"),
            _(u"Other")
            ],
        required=True,
    )

    email = Email(
        title=_(u'Email Address'),
        required=True,
        # contraint=email_constraint,
    )

    emplID = schema.Int(
        title=_(u'Empl ID'),
        description=_(u'Enter your CUNYFirst Empl ID'),
        required=True,
        min=8,
        max=10,
    )

    # Data grid for phoneNumbers
    form.widget(PhoneNumbers=DataGridFieldFactory)
    PhoneNumbers = schema.List(
        title=_(u'Please enter your phone numbers'),
        value_type=DictRow(title=_(u'Phone Numbers'), schema=IPhoneNumbers),
        required=False,
    )

    address = schema.TextLine(
        title=_(u'Address'),
        description=_(u'Enter your home address, including apartment number'),
        required=True,
    )

    city = schema.TextLine(
        title=_(u'City'),
        required=True,
    )

    zipCode = schema.Int(
        title=_(u'Zip Code'),
        description=_(u'Enter your 5 digit zip code'),
        required=True,
        min=5,
        max=5
    )

    birthday = schema.Date(
        title=(u'Date of Birth'),
        required=True
    )

    # Data grid for semester and year
    form.widget(PhoneNumbers=DataGridFieldFactory)
    semesterInfo = schema.List(
        title=_(u'Please enter your phone numbers'),
        value_type=DictRow(title=_(u'Semester and Year'), schema=ISemester),
        required=False,
    )

    professor = schema.TextLine(
        title=_(u'Name of Professor'),
        required=True,
    )

    courseNumSection = schema.TextLine(
        title=_(u'Course Number and Section'),
        description=_(u'Ex: CHEM 101'),
        required=True,
    )

    studentStatement = field.NamedFile(
        title=_(u'Personal Statement'),
        required=False,
    )


    # class ITableRowSchema(interface.Interface):
    #     """DataGrid Test"""

    #     cellPhone = schema.TextLine(title=u"Phone Number (Cell)")
    #     homePhone = schema.TextLine(title=u"Phone Number (Home)")
    #     three = schema.TextLine(title=u"Three")


    # class IFormSchema(interface.Interface):
    #     """DataGrid Schema Test"""

    #     four = schema.TextLine(title=u"Four")
    #     table = schema.List(
    #         title=u"Table",
    #         value_type=DictRow(
    #             title=u"tablerow",
    #             schema=ITableRowSchema
    #         )
    #     )

    # @component.adapter(IFormSchema)
    # class EditForm(form.EditForm):
    #     """I think this is for editing"""

    #     fields = field.Fields(IFormSchema)
    #     label=u"Demo Usage of DataGridField"

    #     fields['table'].widgetFactory = DataGridFieldFactory
        