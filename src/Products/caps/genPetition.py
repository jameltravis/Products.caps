# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from zope import schema
from zope import interface
from plone.supermodel import model
from plone import schema
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from z3c.form import field
from z3c.form import form
from z3c.form.form import extends


# def email_constraint(value):
#     """Email validation of string field"""

#     if "@" and "." not in value:
#         raise zope.interface.Invalid(u'Please enter a valid email address')
#     return True


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
        values=[_(u"Extension INC"), _(u"Grade Appeal"), _(u"Grade Change"), _(u"Other")],
        required=True,
    )

    email = schema.Email(
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

    class ITableRowSchema(interface.Interface):
        """Seems to  be for the setup of 'rows'"""

        cellPhone = schema.TextLine(title=u"Phone Number (Cell)")
        homePhone = schema.TextLine(title=u"Phone Number (Home)")
        three = schema.TextLine(title=u"Three")


    class IFormSchema(interface.Interface):
        """When I figure out what this class is for, I'll let you know"""

        four = schema.TextLine(title=u"Four")
        table = schema.List(
            title=u"Table",
            value_type=DictRow(
                title=u"tablerow",
                schema=ITableRowSchema
            )
        )

    @component.adapter(IFormSchema)
    class EditForm(form.EditForm):
        """I think this is for editing"""

        fields = field.Fields(IFormSchema)
        label=u"Demo Usage of DataGridField"

        fields['table'].widgetFactory = DataGridFieldFactory
        