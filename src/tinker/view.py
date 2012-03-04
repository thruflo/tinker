# -*- coding: utf-8 -*-

""""""

from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.security import authenticated_userid
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from tinker import schema, model

@view_config(route_name='index', renderer='index.mako', permission=NO_PERMISSION_REQUIRED)
def index_view(request):
    return {}


@view_config(route_name='foo', renderer='foo.mako')
def foo_view(request):
    return {}


@view_config(context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED)
def forbidden_view(request):
    """Called when a user has been denied access to a resource or view.  
      
      If the user is already logged in, it means they don't have the requisit
      permission, so we raise a 403 Forbidden error.  Otherwise we redirect
      to the login page.
    """
    
    if authenticated_userid(request):
        return HTTPForbidden()
    url = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=url)


@view_config(route_name='login', request_method='POST', xhr=True, renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def authenticate_view(request):
    """If posted a ``username`` and ``password``, attempt to authenticate the
      user using the credentials provided.  If authentication if successful, 
      return the JSON representation of the authenticated user.
    """
    
    form = Form(request, schema=schema.Authenticate)
    if form.validate():
        user = model.User.authenticate(**form.data)
        if user:
            remember(request, user.canonical_id)
            return user.__json__()
    return {}


@view_config(route_name='login', xhr=False, renderer='login.mako', 
             permission=NO_PERMISSION_REQUIRED)
def login_view(request):
    """Render login form.  If posted a ``username`` and ``password``, attempt to
      authenticate the user using the credentials provided.  If authentication
      if successful, redirect the user whence they came.
    """
    
    next = request.params.get('next') or request.route_url('index')
    defaults = {
        'failed': False, 
        'next': next
    }
    form = Form(request, schema=schema.Login, defaults=defaults)
    if request.method == 'POST':
        if form.validate():
            credentials = {
                'username': form.data['username'],
                'password': form.data['password']
            }
            user = model.User.authenticate(**credentials)
            if user:
                headers = remember(request, user.canonical_id)
                return HTTPFound(location=next, headers=headers)
        form.data['failed'] = True
    return {'renderer': FormRenderer(form)}


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    url = request.route_url('index')
    return HTTPFound(location=url, headers=headers)

