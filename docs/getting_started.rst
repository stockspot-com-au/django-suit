Getting Started
===============

Installation
------------


Requirements: Python 3.10+ and Django 4.2, 5.2 (LTS), 6.0 or 6.1.

1. Install this fork with pip::

    pip install https://github.com/mhindery/django-suit/archive/develop.zip

2. You will need to add the ``'suit'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        ...
        'suit',
        'django.contrib.admin',
    )

  .. important:: ``'suit'`` must be added before ``'django.contrib.admin'`` and before any third-party app that ships its own admin templates.

3. Make sure you have ``django.template.context_processors.request`` in your ``TEMPLATES`` ``OPTIONS`` ``context_processors`` setting in your Django project ``settings.py`` file.::


      TEMPLATES = [
          {
              'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [],
              'APP_DIRS': True,
              'OPTIONS': {
                  'context_processors': [
                      'django.template.context_processors.debug',
                      'django.template.context_processors.request', # Make sure you have this line
                      'django.contrib.auth.context_processors.auth',
                      'django.contrib.messages.context_processors.messages',
                  ],
              },
          },
      ]


  Note: This is required to handle left side menu. If by some reason you removed original Django Suit ``menu.html``, you can skip this.


Deployment
----------

Deployment with Django Suit should not be different than any other Django application. If you have problems with deployment on production, read `Django docs on wsgi <https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/>`_ first.

.. note:: If you deploy your project with Apache or ``Debug=False`` don't forget to run ``./manage.py collectstatic``


Develop branch
--------------

`Develop branch <https://github.com/darklow/django-suit/commits/develop>`_ is considered as release candidate version. Check `commits <https://github.com/darklow/django-suit/commits/develop>`_ and `changelog <https://github.com/darklow/django-suit/blob/develop/CHANGELOG.rst>`_ of develop branch first, before installing develop version. It is quite stable and always tested, but can contain some flaws or behaviour changes too. To install latest develop version use::

  pip uninstall django-suit
  pip install https://github.com/darklow/django-suit/tarball/develop


Upgrading from 0.3.x
--------------------

0.4.0 moves the theme from Bootstrap 2 to Bootstrap 5 and drops support for Django < 4.2. See the 0.4.0 entry of the `changelog <https://github.com/mhindery/django-suit/blob/develop/CHANGELOG.rst>`_ for what to check in your own admin templates and CSS.

