
"""Module for CAPS Grade change form."""

from Products.caps import _
from Products.caps.validators import choice_constraint, name_check_constraint, email_constraint
from Products.caps.interfaces import ISemester, ICommitteeVote
from plone.supermodel import model, directives
from plone.autoform import directives as permission
from plone.directives import form
from plone.namedfile import field
from zope import schema
from collective.z3cform.datagridfield import DictRow
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory


class IGradeChange(model.Schema):
    """Class to create Grade Appeal schema"""

    title = schema.TextLine(
        title=(u'Name'),
        description=(u'Please enter your First and Last Name'),
        required=True,
        constraint=name_check_constraint,
    )

    petitionReason = schema.Choice(
        title=(u'Reason for Peition'),
        values=[
            (u"Select One"),
            (u"Extension INC"),
            (u"Grade Appeal"),
            (u"Grade Change"),
            (u"Other")
            ],
        required=True,
        constraint=choice_constraint
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

    # Create new fieldset for Committee Approval Field
    directives.fieldset(
        'Staff Only',
        fields=[
            'committeeApproval',
            ]
        )

    # Permissions-dependent field for Committee to see who has
    # note each member's 'vote' on a specific petition
    permission.read_permission(committeeApproval='cmf.ModifyPortalContent')
    permission.write_permission(committeeApproval='cmf.ModifyPortalContent')
    form.widget(committeeApproval=DataGridFieldFactory)
    committeeApproval = schema.List(
        title=(u'Committee Member Votes'),
        value_type=DictRow(
            title=(u'Please enter your name and vote'),
            schema=ICommitteeVote
            ),
        # required=True,
    )