# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IProductsCapsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICAPS(Interface):
    """Marker interface for CAPS dashboard"""
