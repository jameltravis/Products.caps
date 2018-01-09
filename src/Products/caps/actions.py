"""form action stuffs - Work in Progress"""

from AccessControl import getSecurityManager
from BTrees.IOBTree import IOBTree
from BTrees.LOBTree import LOBTree as SavedDataBTree
from Products.caps import _
# from Products.caps.api import dollar_replacer
# from Products.caps.api import filter_fields
# from Products.caps.api import format_addresses
from Products.caps.api import get_context
# from Products.caps.api import get_expression
from Products.caps.api import get_schema
from Products.caps.api import is_file_data
# from Products.caps.api import lnbr
# from Products.caps.api import OrderedDict
from Products.caps.interfaces import IAction
from Products.caps.interfaces import IActionFactory
from Products.caps.interfaces import ICustomScript
from Products.caps.interfaces import IExtraData
# from Products.caps.interfaces import IMailer
from Products.caps.interfaces import ISaveData
from copy import deepcopy
from csv import writer as csvwriter
from DateTime import DateTime
# from email import Encoders
# from email.Header import Header
# from email.MIMEAudio import MIMEAudio
# from email.MIMEBase import MIMEBase
# from email.MIMEImage import MIMEImage
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.utils import formataddr
from logging import getLogger
from plone import api
from plone.autoform.view import WidgetsView
from plone.supermodel.exportimport import BaseHandler
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.PythonScripts.PythonScript import PythonScript
from StringIO import StringIO
from time import time
from z3c.form.interfaces import DISPLAY_MODE
from zope.component import queryUtility
from zope.contenttype import guess_content_type
from zope.interface import implementer
from zope.schema import Bool
from zope.schema import getFieldsInOrder
from zope.security.interfaces import IPermission


logger = getLogger('Products.caps')


@implementer(IActionFactory)
class ActionFactory(object):
    """Unfotunately, I'm not quite sure what this class is for"""

    title = u''

    def __init__(self, fieldcls, title, permission, *args, **kw):
        self.fieldcls = fieldcls
        self.title = title
        self.permission = permission
        self.args = args
        self.kw = kw

    def available(self, context):
        """ field is addable in the current context """
        securityManager = getSecurityManager()
        permission = queryUtility(IPermission, name=self.permission)
        if permission is None:
            return True
        return bool(securityManager.checkPermission(permission.title, context))

    def editable(self, field):
        """ test whether a given instance of a field is editable """
        return True

    def __call__(self, *args, **kw):
        kwargs = deepcopy(self.kw)
        kwargs.update(**kw)
        return self.fieldcls(*(self.args + args), **kwargs)


@implementer(IAction)
class Action(Bool):
    """ Base action class """

    def onSuccess(self, fields, request):
        """Raise Error message that the action was not implemented"""
        raise NotImplementedError(
            "There is not implemented 'onSuccess' of {0!r}".format(self))



@implementer(ICustomScript)
class CustomScript(Action):
    __doc__ = ICustomScript.__doc__

    def __init__(self, **kw):
        for i, f in ICustomScript.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(CustomScript, self).__init__(**kw)

    def getScript(self, context):
        """Generate Python script object"""

        body = self.ScriptBody
        role = self.ProxyRole
        script = PythonScript(self.__name__)
        script = script.__of__(context)

        # Skip check roles
        script._validateProxy = lambda i=None: None

        # Force proxy role
        if role != u'none':
            script.manage_proxy((role,))

        body = body.encode('utf-8')
        params = 'fields, easyform, request'
        script.ZPythonScript_edit(params, body)
        return script

    def sanifyFields(self, form):
        # Makes request.form fields accessible in a script
        #
        # Avoid Unauthorized exceptions since request.form is inaccesible

        result = {}
        for field in form:
            result[field] = form[field]
        return result

    def checkWarningsAndErrors(self, script):
        """
        Raise exception if there has been bad things with the script
        compiling
        """

        if len(script.warnings) > 0:
            logger.warn('Python script ' + self.__name__ +
                        ' has warning:' + str(script.warnings))

        if len(script.errors) > 0:
            logger.error('Python script ' + self.__name__ +
                         ' has errors: ' + str(script.errors))
            raise ValueError(
                'Python script {0} has errors: {1}'.format(
                    self.__name__, str(script.errors)
                )
            )

    def executeCustomScript(self, result, form, req):
        # Execute in-place script

        # @param result Extracted fields from request.form
        # @param form EasyForm object

        script = self.getScript(form)
        self.checkWarningsAndErrors(script)
        response = script(result, form, req)
        return response

    def onSuccess(self, fields, request):
        # Executes the custom script
        form = get_context(self)
        resultData = self.sanifyFields(request.form)
        return self.executeCustomScript(resultData, form, request)


@implementer(ISaveData)
class SaveData(Action):
    __doc__ = ISaveData.__doc__

    def __init__(self, **kw):
        for i, f in ISaveData.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(SaveData, self).__init__(**kw)

    @property
    def _storage(self):
        context = get_context(self)
        if not hasattr(context, '_inputStorage'):
            context._inputStorage = {}
        if self.__name__ not in context._inputStorage:
            context._inputStorage[self.__name__] = SavedDataBTree()
        return context._inputStorage[self.__name__]

    def clearSavedFormInput(self):
        """convenience method to clear input buffer"""
        self._storage.clear()

    def getSavedFormInput(self):
        """ returns saved input as an iterable;
            each row is a sequence of fields.
        """

        return self._storage.values()

    def getSavedFormInputItems(self):
        """ returns saved input as an iterable;
            each row is an (id, sequence of fields) tuple
        """
        return self._storage.items()

    def getSavedFormInputForEdit(self, header=False, delimiter=','):
        """ returns saved as CSV text """
        sbuf = StringIO()
        writer = csvwriter(sbuf, delimiter=delimiter)
        names = self.getColumnNames()
        titles = self.getColumnTitles()

        if header:
            encoded_titles = []
            for t in titles:
                if isinstance(t, unicode):
                    t = t.encode('utf-8')
                encoded_titles.append(t)
            writer.writerow(encoded_titles)
        for row in self.getSavedFormInput():
            def get_data(row, i):
                """get the data in a given row"""
                data = row.get(i, '')
                if is_file_data(data):
                    data = data.filename
                if isinstance(data, unicode):
                    return data.encode('utf-8')
                return data
            writer.writerow([get_data(row, i) for i in names])
        res = sbuf.getvalue()
        sbuf.close()
        return res

    def getColumnNames(self):
        # """Returns a list of column names"""
        context = get_context(self)
        showFields = getattr(self, 'showFields', [])
        if showFields is None:
            showFields = []
        names = [
            name
            for name, field in getFieldsInOrder(get_schema(context))
            if not showFields or name in showFields
        ]
        if self.ExtraData:
            for f in self.ExtraData:
                names.append(f)
        return names

    def getColumnTitles(self):
        """Returns a list of column titles"""
        context = get_context(self)
        showFields = getattr(self, 'showFields', [])
        if showFields is None:
            showFields = []

        names = [
            field.title
            for name, field in getFieldsInOrder(get_schema(context))
            if not showFields or name in showFields
        ]
        if self.ExtraData:
            for f in self.ExtraData:
                names.append(IExtraData[f].title)
        return names

    def download_csv(self, response):
        """Download the saved data as csv
        """
        response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}.csv"'.format(self.__name__)
        )
        response.setHeader('Content-Type', 'text/comma-separated-values')
        response.write(self.getSavedFormInputForEdit(
            getattr(self, 'UseColumnNames', False), delimiter=','))

    def download_tsv(self, response):
        # """Download the saved data as tsv
        # """
        response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}.tsv"'.format(self.__name__)
        )
        response.setHeader('Content-Type', 'text/tab-separated-values')
        response.write(self.getSavedFormInputForEdit(
            getattr(self, 'UseColumnNames', False), delimiter='\t'))

    def download(self, response):
        """Download the saved data
        """
        format = getattr(self, 'DownloadFormat', 'tsv')
        if format == 'tsv':
            return self.download_tsv(response)
        else:
            assert format == 'csv', 'Unknown download format'
            return self.download_csv(response)

    def itemsSaved(self):
        return len(self._storage)

    def delDataRow(self, key):
        del self._storage[key]

    def setDataRow(self, key, value):
        # sdata = self.storage[id]
        # sdata.update(data)
        # self.storage[id] = sdata
        self._storage[key] = value

    def addDataRow(self, value):
        storage = self._storage
        if isinstance(storage, IOBTree):
            # 32-bit IOBTree; use a key which is more likely to conflict
            # but which won't overflow the key's bits
            id = storage.maxKey() + 1
        else:
            # 64-bit LOBTree
            id = int(time() * 1000)
            while id in storage:  # avoid collisions during testing
                id += 1
        value['id'] = id
        storage[id] = value

    def onSuccess(self, fields, request):
        """
        saves data.
        """
        # if LP_SAVE_TO_CANONICAL and not loopstop:
        # LinguaPlone functionality:
        # check to see if we're in a translated
        # form folder, but not the canonical version.
        # parent = self.aq_parent
        # if safe_hasattr(parent, 'isTranslation') and \
        # parent.isTranslation() and not parent.isCanonical():
        # look in the canonical version to see if there is
        # a matching (by id) save-data adapter.
        # If so, call its onSuccess method
        # cf = parent.getCanonical()
        # target = cf.get(self.getId())
        # if target is not None and target.meta_type == 'FormSaveDataAdapter':
        # target.onSuccess(fields, request, loopstop=True)
        # return
        data = {}
        showFields = getattr(self, 'showFields', []) or self.getColumnNames()
        for f in fields:
            if f not in showFields:
                continue
            data[f] = fields[f]

        if self.ExtraData:
            for f in self.ExtraData:
                if f == 'dt':
                    data[f] = str(DateTime())
                else:
                    data[f] = getattr(request, f, '')

        self.addDataRow(data)


CustomScriptAction = ActionFactory(
    CustomScript, _
    (u'label_customscript_action', default=u'Custom Script'),
    'Products.caps.AddCustomScripts'
)
SaveDataAction = ActionFactory(
    SaveData, _
    (u'label_savedata_action', default=u'Save Data'),
    'Products.caps.AddDataSavers'
)

CustomScriptHandler = BaseHandler(CustomScript)
SaveDataHandler = BaseHandler(SaveData)
