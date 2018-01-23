"""Module for creating the Committee Dashboard"""

from operator import itemgetter
from Products.Five.browser import BrowserView
from plone import api


class DashView(BrowserView):
    """
    Classs for finding lists of a given petition type.
    """

    def readmission_petitions(self):
        """Readmission petitions"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(portal_type='Readmission')

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return sorted(results, key=itemgetter('review_state'))

    def extra_credit_petitions(self):
        """Petitions for extra credits"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(portal_type='ExtraCredits')

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return sorted(results, key=itemgetter('review_state'))

    def leave_abs_petitions(self):
        """Petitions for Leave of Absence and Retroactive Withdrawals"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(portal_type='LeaveAbs')

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
        return sorted(results, key=itemgetter('review_state'))

    def grade_appeal_petitions(self):
        """Petitions to have a single grade appealed"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(portal_type='GradeAppeal')

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'CreationDate': brain.CreationDate,
                'review_state': brain.review_state
            })
        return sorted(results, key=itemgetter('review_state'))

    def find_readmissions(self):
        """Use portal_catalog this time to find readmission petitions"""
        # get catalog tool to query DB
        catalog = api.portal.get_tool('portal_catalog')
        # Actually Querying the DB
        results = catalog.searchResults(**{'portal_type': 'Readmission'})
        petitions = []
        # Put the query results in a list and get attributes of interest
        for brains in results:
            petitions.append({
                'title': brains.Title,
                'emplID': brains.emplID,
                'CreationDate': brains.CreationDate,
                'review_state': brains.review_state
            })
        return sorted(petitions, key=itemgetter('review_state'))
