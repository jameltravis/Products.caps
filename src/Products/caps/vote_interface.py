# encoding=utf-8
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface

class IVotableLayer(Interface):
    """Marker interface for the Browserlayer
    """

# Ivotable is the marker interface for contenttypes who support this behavior
class IVotable(Interface):
    """Marker interface for contenttypes who support this behavior"""

# This is the behaviors interface. When doing IVoting(object), you receive an
# adapter
class IVoting(model.Schema):
    """Voting behavior interface. When doing IVoting(object), you receive an adapter"""
    if not api.env.debug_mode():
        directives.omitted("votes")
        directives.omitted("voted")

    fieldset(
        'debug',
        label=u'debug',
        fields=('votes', 'voted'),
    )

    votes = schema.Dict(
        title=u"Vote info",
        key_type=schema.TextLine(title=u"Voted number"),
        value_type=schema.Int(title=u"Voted so often"),
        required=False
        )

    voted = schema.List(
        title=u"Vote hashes",
        value_type=schema.TextLine(),
        required=False
        )

    def vote(self, request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """
        if self.already_voted(request):
            raise KeyError("You may not vote twice")
        vote = int(vote)
        self.annotations['voted'].append(self._hash(request))
        votes = self.annotations['votes']
        if vote not in votes:
            votes[vote] = 1
        else:
            votes[vote] += 1


    def average_vote(self):
        """
        Return the average voting for an item
        """

    def has_votes(self):
        """
        Return whether anybody ever voted for this item
        """

    def already_voted(self, request):
        """
        Return the information wether a person already voted.
        This is not very high level and can be tricked out easily
        """

    def clear(self):
        """
        Clear the votes. Should only be called by admins
        """

alsoProvides(IVoting, IFormFieldProvider)
