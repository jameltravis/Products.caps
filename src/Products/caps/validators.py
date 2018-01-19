"""Form validators."""

from Products.caps import _
from zope import interface
from plone import api

def readmission_limit_constraint(value):
    """determine if field value exists in catalog index."""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog.searchResults(**{'portal_type': 'Readmission', 'emplID': value})
    if len(results) > 3:
        raise interface.Invalid(
            _(u"Petition limit exceeded. Please contact osas@york.cuny.edu for further help")
        )
    else:
        return True

def name_check_constraint(value):
    """ensures that student enters at least two words/names"""
    if ' ' not in value:
        raise interface.Invalid(_(u"Please enter your first AND last name"))
    return True

def email_constraint(value):
    """Email validator"""
    if '.' not in value and '@' not in value:
        raise interface.Invalid(_(u"Sorry, you've entered an invalid email address"))
    return True

def choice_constraint(value):
    """if the selection is left on default value, raise error message
    In order for this to work the 1st list item must be a generic choice
    Ex: 'Select One'
    """
    if value == value[0]:
        raise interface.Invalid(_(u"Please select a choice"))
    else:
        return True
