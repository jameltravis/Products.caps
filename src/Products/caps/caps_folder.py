"""A CAPS Folder.

A Folderish object created to house caps forms.
"""

from Products.caps import _
from plone.supermodel import model
from zope import schema

class ICAPSFolder(model.Schema):
    """Class for defaault view for Caps Committee dash"""

    title = schema.TextLine(
        title=(u'Folder title'),
        required=True,
    )

    description = schema.Text(
        title=(u'Description'),
        description=(u'What will be housed in this folder?'),
        required=True
    )
