"""Module for creating the Committee Dashboard"""

from Products.Five.browser import BrowserView
from zope.security import checkPermission

class CommitteeView(BrowserView):
    """Default view for committee members"""

    def canRequestReview(self):
        """check permission so we can display permission-dependant material"""
        return checkPermission('cmf.RequestReview', self.context)