"""Upgrade module for 'Products.caps'.
Far more pythonic now.
"""

import logging
from plone import api

default_profile = 'profile-Products.caps:default'
logger = logging.getLogger(__name__)

def upgrade_site(setup):

    """
    creates CAPS main folder in portal.
    Used to do more but most of this stuff can be done for
    free using Manage Contents and Content Rules.
    """

    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()

    # Create 'CAPS'folder, if needed
    if 'caps' not in portal:
        caps_folder = api.content.create(
            container=portal,
            type='Folder',
            id='caps',
            title=u'CAPS'
        )

    else:
        caps_folder = portal['caps']
