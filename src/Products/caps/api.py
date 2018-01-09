"""EasyForm API adapted for Products.caps"""


# from AccessControl import ClassSecurityInfo
# from App.class_init import InitializeClass
# from collections import OrderedDict as BaseDict
from Products.caps.config import MODEL_DEFAULT
# from Products.caps.interfaces import IFieldExtender
# from email.utils import formataddr
from plone import api
from plone.namedfile.interfaces import INamedBlobFile
from plone.namedfile.interfaces import INamedFile
from plone.supermodel import loadString
from plone.supermodel import serializeSchema
from plone.supermodel.parser import SupermodelParseError
# from Products.CMFCore.Expression import Expression
# from Products.CMFCore.Expression import getExprContext
# from Products.CMFPlone.utils import safe_unicode
from re import compile
# from types import StringTypes
# from zope.schema import getFieldsInOrder


CONTEXT_KEY = u'context'
# regular expression for dollar-sign variable replacement.
# we want to find ${identifier} patterns
dollarRE = compile(r'\$\{(.+?)\}')


def get_context(field):
    """ Get context of field
    :param field: [required] dexterity field
    :returns: content-type-form
    """
    return field.interface.getTaggedValue(CONTEXT_KEY)


def get_model(data, context):
    """get the schema model"""
    schema = None
    # if schema is set on context it has priority
    if data is not None:
        try:
            schema = loadString(data).schema
        except SupermodelParseError:  # pragma: no cover
            pass

    # 2nd we try aquire the model
    if not schema:
        nav_root = api.portal.get_navigation_root(context)
        schema = nav_root.get('easyform_model_default.xml')

    # finally we fall back to the hardcoded example
    if not schema:
        schema = loadString(MODEL_DEFAULT).schema
    schema.setTaggedValue(CONTEXT_KEY, context)
    return schema


# caching this breaks with memcached
def get_schema(context):
    """get the schema"""
    try:
        data = context.fields_model
    except AttributeError:
        data = None
    return get_model(data, context)


# caching this breaks with memcached
def get_actions(context):
    """get actions model"""
    try:
        data = context.actions_model
    except AttributeError:
        data = None
    return get_model(data, context)


def set_fields(context, schema):
    """serialize and store the current schema"""
    # serialize the current schema
    snew_schema = serializeSchema(schema)
    # store the current schema
    context.fields_model = snew_schema
    context.notifyModified()


def set_actions(context, schema):
    """fix seting widgets, serialize current schema and store schema"""
    # fix setting widgets
    schema.setTaggedValue('plone.autoform.widgets', {})
    # serialize the current schema
    snew_schema = serializeSchema(schema)
    # store the current schema
    context.actions_model = snew_schema
    context.notifyModified()


def is_file_data(field):
    """Return True, if field is a file field.
    """
    ifaces = (INamedFile, INamedBlobFile)
    for i in ifaces:
        if i.providedBy(field):
            return True
    return False
