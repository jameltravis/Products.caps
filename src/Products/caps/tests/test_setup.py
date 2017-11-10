# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from Products.caps.testing import PRODUCTS_CAPS_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that Products.caps is properly installed."""

    layer = PRODUCTS_CAPS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if Products.caps is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'Products.caps'))

    def test_browserlayer(self):
        """Test that IProductsCapsLayer is registered."""
        from Products.caps.interfaces import (
            IProductsCapsLayer)
        from plone.browserlayer import utils
        self.assertIn(IProductsCapsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PRODUCTS_CAPS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['Products.caps'])

    def test_product_uninstalled(self):
        """Test if Products.caps is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'Products.caps'))

    def test_browserlayer_removed(self):
        """Test that IProductsCapsLayer is removed."""
        from Products.caps.interfaces import \
            IProductsCapsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IProductsCapsLayer, utils.registered_layers())
