"""Module for creating the Committee Dashboard"""

from operator import itemgetter
from Products.Five.browser import BrowserView
from plone import api
from plone.dexterity.browser.view import DefaultView

class DashView(BrowserView):
    """
    Classs for finding lists of a given petition type.
    """

    def find_readmissions(self):
        """Use portal_catalog this time to find readmission petitions."""
        catalog = api.portal.get_tool('portal_catalog')
        readmissions = catalog.searchResults(**{'portal_type': 'Readmission'})
        petitions = []
        # Put the query results in a list and get attributes of interest
        for brains in readmissions:
            petitions.append({
                'title': brains.Title,
                'emplID': brains.emplID,
                'CreationDate': brains.CreationDate,
                'review_state': brains.review_state
            })
        if not petitions:
            return u'No petitions at the moment'
        else:
            return sorted(petitions, key=itemgetter('review_state'))



class IndexView(BrowserView):
    """Methods for the index page of CAPS."""

    def pending_readmissions(self):
        """returns a list of readmission objects with 'private' review_states."""
        catalog = api.portal.get_tool('portal_catalog')
        readmissions = catalog.searchResults(**{'portal_type': 'Readmission'})
        petitions = [item for item in readmissions if item['review_state'] == 'private']
        if not petitions:
            return 0
        else:
            return len(petitions)


    def pending_extra_credits(self):
        """returns a list of readmission objects with 'private' review_states."""

        catalog = api.portal.get_tool('portal_catalog')
        extra_creds = catalog.searchResults(**{'portal_type': 'ExtraCredits'})
        petitions = [item for item in extra_creds if item['review_state'] == 'private']
        if not petitions:
            return 0
        else:
            return len(petitions)


    def pending_grade_changes(self):
        """returns a list of readmission objects with 'private' review_states."""
        catalog = api.portal.get_tool('portal_catalog')
        grade_change = catalog.searchResults(**{'portal_type': 'GradeChange'})
        petitions = [item for item in grade_change if item['review_state'] == 'private']
        if not petitions:
            return 0
        else:
            return len(petitions)



    def pending_leave_abs(self):
        """returns a list of readmission objects with 'private' review_states."""
        catalog = api.portal.get_tool('portal_catalog')
        leave_abs = catalog.searchResults(**{'portal_type': 'LeaveAbs'})
        petitions = [item for item in leave_abs if item['review_state'] == 'private']
        if not petitions:
            return 0
        else:
            return len(petitions)

class ReadmissionView(DefaultView):
    """Provides readmissionview.pt template
    """
