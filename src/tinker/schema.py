# -*- coding: utf-8 -*-

""""""

import re

import formencode
from formencode import validators

from passlib.apps import custom_app_context as pwd_context

valid_username = re.compile(r'^[.\w-]{1,32}$', re.U)
valid_password = re.compile(r'^(.){7,200}$', re.U)

class Username(validators.UnicodeString):
    """Validates that the user input matches ``valid_username``, strips and
      coerces to lowercase.
    """
    
    messages = {
        'invalid': 'No spaces, no funny chars, upto 32 characters long.'
    }
    
    def _to_python(self, value, state):
        value = super(Username, self)._to_python(value, state)
        return value.lower().strip()
    
    def validate_python(self, value, state):
        super(Username, self).validate_python(value, state)
        if not valid_username.match(value):
            raise validators.Invalid(
                self.message("invalid", state),
                value,
                state
            )
    

class Password(validators.UnicodeString):
    """Validates that the user input matches ``valid_password``, strips and
      coerces to lowercase.
    """
    
    messages = {
        'invalid': 'Must be at least seven characters long.'
    }
    
    def _to_python(self, value, state):
        value = super(RawPassword, self)._to_python(value, state)
        return value.lower().strip()
    
    def validate_python(self, value, state):
        super(RawPassword, self).validate_python(value, state)
        if not valid_password.match(value):
            raise validators.Invalid(
                self.message("invalid", state),
                value,
                state
            )
            
        
    
    


class Authenticate(formencode.Schema):
    """"""
    
    filter_extra_fields = True
    allow_extra_fields = True
    
    username = Username(not_empty=True)
    password = Password(not_empty=True)

class Login(formencode.Schema):
    """"""
    
    filter_extra_fields = True
    allow_extra_fields = True
    
    username = Username(not_empty=True)
    password = Password(not_empty=True)
    
    failed = validators.Bool(not_empty=True)
    next = validators.URL(not_empty=True)

