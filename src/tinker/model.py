# -*- coding: utf-8 -*-

""""""

import logging
from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated, Everyone

from sqlalchemy import Boolean, Column, DateTime, Integer, Unicode

from .base import Base, BaseMixin, Session

class Trunk(object):
    """Root object of the application's resource tree."""
    
    __name__ = None
    
    __acl__ = [
        (Deny, Everyone, ALL_PERMISSIONS),
    ]
    
    def __init__(self, request):
        self.request = request
    
    def __getitem__(self, key):
        raise KeyError
    


class User(Base, BaseMixin):
    """Model class encapsulating an authenticated user."""


def group_finder(user_id, request):
    """Authentication policy callback handler that returns a list of groups
      an authenticated user is a member of.
    """
    
    user = User.get_by_id(user_id)
    if user:
        return [u'g:{0}'.format(g) for g in user.groups]

