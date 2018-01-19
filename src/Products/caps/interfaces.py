# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from Products.caps.validators import choice_constraint
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema


class IProductsCapsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ISemester(model.Schema):
    """Generates 'Semester' DataGridField."""

    semester = schema.Choice(
        title=(u'Semester'),
        values=[
            (u'Select One'),
            (u'Fall'),
            (u'Winter'),
            (u'Spring'),
            (u'Summer'),
        ],
        required=True,
        constraint=choice_constraint,
    )

    semesterYear = schema.TextLine(
        title=(u'Year'),
        required=True,
    )


class IPhoneNumbers(model.Schema):
    """Used for Phone number datagrid"""

    cellPhoneNumber = schema.TextLine(
        title=(u'Phone Number (Cell)'),
        required=False,
    )

    homePhoneNumber = schema.TextLine(
        title=(u'Phone Number (Home)'),
        required=False,
    )


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

