# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.caps import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IReadmission(Interface):

    title = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )
