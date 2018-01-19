"""Module for creating the Committee Dashboard"""

from Products.Five.browser import BrowserView
# from operator import itemgetter
from plone import api


class DashView(BrowserView):
    """
    Class for each petition type
    """

    def readmission_petitions(self):
        """Readmission petitions"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(
            portal_type='Readmission',
            sort_on='review_state',
            sort_order='descending',
        )

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return results

    def extra_credit_petitions(self):
        """Petitions for extra credits"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(
            portal_type='ExtraCredits',
            sort_on='review_state',
            sort_order='descending',
        )

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return results

    def leave_abs_petitions(self):
        """Petitions for Leave of Absence and Retroactive Withdrawals"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(
            portal_type='LeaveAbs',
            sort_on='review_state',
            sort_order='descending',
        )

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return results

    def grade_appeal_petitions(self):
        """Petitions to have a single grade appealed"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(
            portal_type='GradeAppeal',
            sort_on='review_state',
            sort_order='descending',
        )

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return results
