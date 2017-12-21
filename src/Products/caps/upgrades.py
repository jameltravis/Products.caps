# -*- coding: utf-8 -*-
"""Upgrade module for Products.caps .

Upon being run, two directories (folderish objects) will be created at the root level:
Readmission and Student academic Services. The latter will house the following sub
directories: Extra-Credits, Leave of Absence and Grade Appeal.

Readmissions is a stand alone folder because it requires the ability to change permissions
based on an any number of arbitrarly indexed items.

On the off chance that there are content types of interest (CTOI) outside of these folders,
those CTOI are also gathers and put in their associated folders.

Note: At the moment, this code is all or nothing.
"""

import logging
from plone import api

default_profile = 'profile-Products.caps:default'
logger = logging.getLogger(__name__)

def upgrade_site(setup):

    """
    creates CAPS main folder in portal, extra-credits folder in CAPS,
    grade-appeals folder in CAPS, loa-petition portal in CAPS,
    and readmission folder in portal
    """

    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()

    # Create 'CAPS'folder, if needed
    if 'caps' and 'readmission' not in portal:
        caps_folder = api.content.create(
            container=portal,
            type='Folder',
            id='caps',
            title=u'CAPS'
        )
        readmission_folder = api.content.create(
            container=portal,
            type='Folder',
            id='readmission',
            title=u'Readmission'
        )
    else:
        caps_folder = portal['caps']
        readmission_folder = portal['readmission']

    # Create 'Extra Credits' folder in 'CAPS', if needed
    if 'extra-credits' and 'grade-appeals' and 'loa-petitions' not in caps_folder:
        extraCredits_folder = api.content.create(
            container=caps_folder,
            type='Folder',
            id='extra-credits',
            title=u'Extra Credits',
        )
        gradeAppeal_folder = api.content.create(
            container=caps_folder,
            type='Folder',
            id='grade-appeals',
            title=u'Grade Appeals',
        )
        loa_folder = api.content.create(
            container=caps_folder,
            type='Folder',
            id='loa-petitions',
            title=u'Leave of Absence',
        )
    else:
        extraCredits_folder = caps_folder['extra-credits']
        gradeAppeal_folder = caps_folder['Grade Appeals']
        loa_folder = caps_folder['loa-petitions']

    # Put Readmission objects in readmission folder
    brainsReadmission = api.content.find(portal_type='Readmission')
    for brainsReadmission in brainsReadmission:
        if Readmission_url in brainsReadmission.getURL():
            # skip if content type is already in target folder
            continue
        # Keeping you in the loop of what is happening
        obj = brainsReadmission.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), readmission_folder.absolute_url()
        ))
        # Actually moving Readmission content type to readmission folder
        api.content.move(
            source=obj,
            target=readmission_folder,
            safe_id=True,
        )

    # Put Extra Credits objects in readmission folder
    brainsExtraCredits = api.content.find(portal_type='ExtraCredits')
    for brainsExtraCredits in brainsExtraCredits:
        if ExtraCredits_url in brainsExtraCredits.getURL():
            continue
        obj = brainsExtraCredits.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), extraCredits_folder.absolute_url()
        ))
        api.content.move(
            source=obj,
            target=extraCredits_folder,
            safe_id=True,
        )

    # Put LOA objects in coresponding folder
    brainsLOA = api.content.find(portal_type='LeaveAbs')
    for brainsLOA in brainsLOA:
        if LeaveAbs_url in brainsLOA.getURL():
            continue
        obj = brainsLOA.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), loa_folder.absolute_url()
        ))
        api.content.move(
            source=obj,
            target=loa_folder,
            safe_id=True,
        )

    # Put GradeAppeal objects in coresponding folder
    brainsGradeAppeal = api.content.find(portal_type='GradeAppeal')
    for brainsGradeAppeal in brainsGradeAppeal:
        if GradeAppeal_url in brainsGradeAppeal.getURL():
            continue
        obj = brainsGradeAppeal.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), gradeAppeal_folder.absolute_url()
        ))
        api.content.move(
            source=obj,
            target=gradeAppeal_folder,
            safe_id=True,
        )
