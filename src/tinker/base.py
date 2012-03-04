# -*- coding: utf-8 -*-

"""Abstracts some SQLAlchemy boilerplate out of the ``model.py`` module."""

__all__ = [
    'Base',
    'BaseMixin',
    'Session'
]

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Integer, MetaData, desc
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def snip(instance, name, limit):
    """Truncate a string value if it's longer than ``limit``."""
    
    value = getattr(instance, name, None)
    if not value:
        return u''
    value = unicode(value)
    if len(value) < limit:
        return value
    return u'{} …'.format(value[:limit])


class BaseMixin(object):
    """Provides an int ``id`` as primary key, ``version``, ``created`` ``modified``
      columns and a scoped ``self.query`` property.
    """
    
    id =  Column(Integer, primary_key=True)
    
    version = Column('v', Integer, default=1)
    created = Column('c', DateTime, default=datetime.utcnow)
    modified = Column('m', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    query = Session.query_property()
    
    @declared_attr
    def __tablename__(cls):
        return u'{0}s'.format(cls.__name__.lower())
    
    def __json__(self):
        d = {'__name__': self.__class__.__name__.lower()}
        for k in self.__public__:
            v = getattr(self, k)
            if isinstance(v, datetime):
                v = v.isoformat()
            elif isinstance(v, Decimal):
                v = float(v)
            elif hasattr(v, '__json__'):
                v = v.__json__()
            else:
                try:
                    unicode(v)
                except TypeError:
                    continue
            d[k] = v
        return d
    
    @property
    def __public__(self):
        return self.__table__.c.keys()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by(cls, name, value):
        kwargs = {}
        kwargs[name] = value
        query = cls.query.filter_by(**kwargs)
        return query.first()
    
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.c.desc())
        return query.all()
    
    def __unicode__(self):
        attrs = [u'{0}="{1}"'.format(k, snip(k, 50)) for k in self.__public__]
        return u'<{0} {1} />'.format(self.__class__.__name__, ' '.join(attrs))
    
    def __repr__(self):
        return unicode(self)
    

