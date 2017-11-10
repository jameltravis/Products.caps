# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import Products.caps


class ProductsCapsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=Products.caps)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.caps:default')


PRODUCTS_CAPS_FIXTURE = ProductsCapsLayer()


PRODUCTS_CAPS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PRODUCTS_CAPS_FIXTURE,),
    name='ProductsCapsLayer:IntegrationTesting'
)


PRODUCTS_CAPS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PRODUCTS_CAPS_FIXTURE,),
    name='ProductsCapsLayer:FunctionalTesting'
)


PRODUCTS_CAPS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PRODUCTS_CAPS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ProductsCapsLayer:AcceptanceTesting'
)
