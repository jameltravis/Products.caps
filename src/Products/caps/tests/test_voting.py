import unittest
import tempfile
import ZODB
import transaction
from persistent import Persistent
from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations


class Dummy(Persistent):
    implements(IAttributeAnnotatable)


class RequestDummy(object):

    def __init__(self, ip, headers=None):
        self.ip = ip
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {
                'User-Agent': 'foo',
                'Accept-Language': 'bar',
                'Accept-Encoding': 'baz'
                }

    def getClientAddr(self):
        return self.ip

    def getHeader(self, key):
        return self.headers[key]


class VotingTests(unittest.TestCase):

    def test_voting_conflict(self):
        from starzel.votable_behavior.behavior.voting import Vote
        dbname = tempfile.mktemp()
        db = ZODB.DB(dbname)
        tm_A = transaction.TransactionManager()
        conn_A = db.open(transaction_manager=tm_A)
        p_A = conn_A.root()['voting'] = Vote(AttributeAnnotations(Dummy()))
        tm_A.commit()
        # Now get another copy of 'p' so we can make a conflict.
        # Think of `conn_A` (connection A) as one thread, and
        # `conn_B` (connection B) as a concurrent thread.  `p_A`
        # is a view on the object in the first connection, and `p_B`
        # is a view on *the same persistent object* in the second connection.
        tm_B = transaction.TransactionManager()
        conn_B = db.open(transaction_manager=tm_B)
        p_B = conn_B.root()['voting']
        assert p_A.context.obj._p_oid == p_B.context.obj._p_oid
        # Now we can make a conflict, and see it resolved (or not)
        request_A = RequestDummy('192.168.0.1')
        p_A.vote(1, request_A)
        request_B = RequestDummy('192.168.0.5')
        p_B.vote(2, request_B)
        tm_B.commit()
        tm_A.commit()