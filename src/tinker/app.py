# -*- coding: utf-8 -*-

"""Provides the main application entry points:
  
  * ``factory()`` is a WSGI application factory
  * ``bootstrap()`` bootstraps the database
  
"""

import sys

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.paster import get_appsettings
#from pyramid.request import Request
#from pyramid.view import AppendSlashNotFoundViewFactory
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from .model import Base, Session, Trunk, group_finder
#from .views import get_is_authenticated, get_user
#from .views import not_found_view

def factory(global_config, **settings):
    """Call with settings to create and return a WSGI application."""
    
    # Bind the SQLAlchemy model classes to the database specified in the
    # ``settings`` provided.
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    
    # Initialise the ``Configurator`` with the ``settings`` provided.
    authn_policy = SessionAuthenticationPolicy(callback=group_finder, debug=True)
    authz_policy = ACLAuthorizationPolicy()
    kwargs = {
        'authentication_policy': authn_policy,
        'authorization_policy': authz_policy,
        'default_permission': 'view',
        'settings': settings, 
        'root_factory': Trunk
    }
    config = Configurator(**kwargs)
    config.include('pyramid_beaker')
    config.include('pyramid_tm')
    config.include('pyramid_weblayer')
    config.set_session_factory(session_factory_from_settings(settings))
    
    # Expose routes.
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('foo', '/foo')
    
    # Add ``is_authenticated`` and ``user`` properties to the request.
    #config.set_request_property(get_is_authenticated, 'is_authenticated', reify=True)
    #config.set_request_property(get_user, 'user', reify=True)
    
    # Configure a custom 404 that first tries to append a slash to the URL.
    #not_found = AppendSlashNotFoundViewFactory(not_found_view)
    #config.add_view(not_found, context='pyramid.httpexceptions.HTTPNotFound')
    
    # Run a venusian scan to pick up the declerative configuration.
    config.scan()
    
    # Return a configured WSGI application.
    return config.make_wsgi_app()

def bootstrap(settings=None):
    """Populate the database from scratch."""
    
    if settings is None:
        if len(sys.argv) != 2:
            sys.exit('usage: {0} etc/config_file.ini'.format(sys.argv[0]))
        settings = get_appsettings(sys.argv[1])
    
    # Configure an SQLAlchemy engine using the config file listed on the
    # command line.
    engine = engine_from_config(settings, 'sqlalchemy.')
    
    # Use the engine to drop and then create all the tables in the db.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    # Bind the scoped database session factory to the engine.
    Session.configure(bind=engine)
    
    # XXX do foo.

