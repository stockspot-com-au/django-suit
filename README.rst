===========
Project status
===========

This is a fork of the unmaintaned upstream `django-suit <https://github.com/darklow/django-suit>`_ project. The `develop` branch is compatible with the latest Django versions, other branches were left as-is on the moment of forking.

Version 0.4 supports Django 5.2 (LTS), 6.0 and 6.1 on Python 3.10+, and uses Bootstrap 5.3, Bootstrap Icons and the jQuery shipped with Django admin (3.7.1). See ``CHANGELOG.rst`` before upgrading from 0.3.

Install this using pip and direct github, it is not published on pypi as separate package currently:

```
pip install https://github.com/mhindery/django-suit/archive/develop.zip
```

===========
Django Suit
===========

**Modern theme for Django admin interface**.

Django Suit is alternative theme/skin/extension for `Django <http://www.djangoproject.com>`_ administration interface.

* Project home: http://djangosuit.com/
* Live demo: http://djangosuit.com/admin/


License
=======

* Django Suit is licensed under `Creative Commons Attribution-NonCommercial 3.0 <http://creativecommons.org/licenses/by-nc/3.0/>`_ license.
* Licence and pricing: http://djangosuit.com/pricing/


Docs & Support
==============

* Documentation: http://django-suit.readthedocs.org/
* Support: http://djangosuit.com/support/
* `Demo app <http://djangosuit.com/admin/>`_ repository is here: `django-suit-examples <https://github.com/darklow/django-suit-examples>`_
* IRC Channel: Feel free to join us at ``#django-suit`` on ``irc.freenode.net`` for a chat
* Follow `on Twitter <http://twitter.com/DjangoSuit>`_ to get latest news

Changelog
=========

See `CHANGELOG.rst <https://github.com/darklow/django-suit/blob/develop/CHANGELOG.rst>`_.


Contributing
============

See `Contributing documentation <http://django-suit.readthedocs.org/en/develop/contributing.html>`_


Tests
=====

Tests run on GitHub Actions for Django 5.2, 6.0 and 6.1 (see ``.github/workflows/tests.yml``). To run them locally::

    python manage.py test suit.tests


Preview
=======

.. image:: https://raw.github.com/darklow/django-suit/develop/docs/_static/img/django-suit.png
   :alt: Django Suit Preview
   :target: http://djangosuit.com/admin/


v2.0-dev
========

Check out new v2.0-dev version notes: https://github.com/darklow/django-suit/issues/475
