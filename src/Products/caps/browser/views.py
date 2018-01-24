"""Classes for binding views.

Use python in templates to generate stuffs.
"""

from operator import itemgetter
from Products.Five.browser import BrowserView
from plone import api


class DashView(BrowserView):
    """
    Classs for finding lists of a given petition type.
    """

    # def find_readmissions(self):
    #     """Use portal_catalog this time to find readmission petitions."""
    #     petitions = []
    #     # Put the query results in a list and get attributes of interest
    #     for brains in READMISSIONS:
    #         petitions.append({
    #             'title': brains.Title,
    #             'emplID': brains.emplID,
    #             'CreationDate': brains.CreationDate,
    #             'review_state': brains.review_state
    #         })
    #     return sorted(petitions, key=itemgetter('review_state'))

class IndexView(BrowserView):
    """Methods for the index page of CAPS."""

    # def pending_readmissions(self):
    #     """returns a list of readmission objects with 'private' review_states."""

    #     return filter(lambda READMISSIONS: READMISSIONS['review_state'] == 'private', READMISSIONS)


    # def pending_extra_credits(self):
    #     """returns a list of extra_credits objects with 'private' review_states."""

    #     return filter(lambda EXTRA_CREDS: EXTRA_CREDS['review_state'] == 'private', EXTRA_CREDS)


    # def pending_grade_changes(self):
    #     """returns a list of grade_change objects with 'private' review_states."""

    #     return filter(lambda GRADE_CHANGE: GRADE_CHANGE['review_state'] == 'private', GRADE_CHANGE)


    # def pending_leave_abs(self):
    #     """returns a list of leave_abs objects with 'private' review_states."""

    #     return filter(lambda LEAVE_ABS: LEAVE_ABS['review_state'] == 'private', LEAVE_ABS)


