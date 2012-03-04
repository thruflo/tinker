<%inherit file="layout.mako"/>
<%namespace name="form" file="form.mako" />

${renderer.begin(request.resource_url(request.root, 'login'))}
  ${renderer.csrf_token()}
  ${renderer.hidden("next")}
  % if renderer.form.data['failed']:
    <div class="alert alert-error">
      Authentication failed.
    </div>
  % endif
  ${form.field(renderer, 'text', 'username')}
  ${form.field(renderer, 'password', 'password')}
  <div class="buttons">
    ${renderer.submit("submit", "Login")}
  </div>
${renderer.end()}
