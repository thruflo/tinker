<!DOCTYPE HTML>
<html>
  <head>
    <meta charset="utf-8" />
    <title>
      Tinker
    </title>
  </head>
  <body>
    <div class="topbar">
      <div class="topbar-inner">
        <div class="container-fluid">
          <a class="brand" href="/">Tinker</a>
          <ul class="nav">
            <li>
              <a href="/">Index</a>
            </li>
            <li>
              <a href="/foo">Foo</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div id="main-content" class="container-fluid">
      ${next.body()}
    </div>
  </body>
</html>