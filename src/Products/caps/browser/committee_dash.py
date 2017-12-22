"""Module for creating the Committee Dashboard"""

from Products.Five.browser import BrowserView
from zope.security import checkPermission
from plone import api


class DashView(BrowserView):
    """
    Depending on the role of the staff viewing the petitions,
    they will see workflow state-based content
    """

    def canRequestReview(self):
        """check permission so we can display permission-dependant material"""
        return checkPermission('cmf.RequestReview', self.context)

    def readmission_petitions(self):
        """Readmission petitions"""

        results = []
        # catalog = api.portal.get_tool('portal_catalog')
        brains = api.content.find(
            portal_type='Readmission',
            sort_on='start',
            sort_order='descending',
        )

        for brain in brains:
            results.append({
                'title': brain.Title,
                'emplID': brain.emplID,
                'review_state': brain.review_state
            })
            return results
        