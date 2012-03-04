from setuptools import setup, find_packages

setup(
    name='tinker',
    version='0.1',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='James Arthur',
    author_email='username: thruflo, domain: gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'pyramid',
        'pyramid_beaker',
        'pyramid_debugtoolbar',
        'pyramid_simpleform',
        'pyramid_tm',
        'pyramid_weblayer',
        'transaction',
        'waitress',
        'zope.sqlalchemy',
        'SQLAlchemy',
        'psycopg2',
        'formencode',
        'passlib',
        'PyCrypto',
        # Imaging, e.g.: http://dist.repoze.org/PIL-1.1.6.tar.gz
        #'pyramid_assetgen',
        #'assetgen',
        #'formencode',
        #'python-postmark',
        #'pyDNS',
        #'python-dateutil',
        'setuptools-git',
    ],
    entry_points = """\
        [setuptools.file_finders]
        ls = setuptools_git:gitlsfiles
        [paste.app_factory]
        main = tinker.app:factory
        [console_scripts]
        tinker_bootstrap_db = tinker.app:bootstrap
    """,
)
