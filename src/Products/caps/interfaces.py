# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from Products.caps.validators import choice_constraint
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema
from zope.interface import alsoProvides, Interface


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

# class IVotableLayer(Interface):
#     """Marker interface for the Browserlayer
#     """

# # Ivotable is the marker interface for contenttypes who support this behavior
# class IVotable(Interface):
#     """Marker interface for contenttypes who support this behavior"""

# # This is the behaviors interface. When doing IVoting(object), you receive an
# # adapter
# class IVoting(model.Schema):
#     """Voting behavior interface. When doing IVoting(object), you receive an adapter"""
#     if not api.env.debug_mode():
#         directives.omitted("votes")
#         directives.omitted("voted")

#     fieldset(
#         'debug',
#         label=u'debug',
#         fields=('votes', 'voted'),
#     )

#     votes = schema.Dict(
#         title=u"Vote info",
#         key_type=schema.TextLine(title=u"Voted number"),
#         value_type=schema.Int(title=u"Voted so often"),
#         required=False
#         )

#     voted = schema.List(
#         title=u"Vote hashes",
#         value_type=schema.TextLine(),
#         required=False
#         )

#     def vote(self, request):
#         """
#         Store the vote information, store the request hash to ensure
#         that the user does not vote twice
#         """
#         if self.already_voted(request):
#             raise KeyError("You may not vote twice")
#         vote = int(vote)
#         self.annotations['voted'].append(self._hash(request))
#         votes = self.annotations['votes']
#         if vote not in votes:
#             votes[vote] = 1
#         else:
#             votes[vote] += 1


#     def average_vote(self):
#         """
#         Return the average voting for an item
#         """

#     def has_votes(self):
#         """
#         Return whether anybody ever voted for this item
#         """

#     def already_voted(self, request):
#         """
#         Return the information wether a person already voted.
#         This is not very high level and can be tricked out easily
#         """

#     def clear(self):
#         """
#         Clear the votes. Should only be called by admins
#         """

# alsoProvides(IVoting, IFormFieldProvider)