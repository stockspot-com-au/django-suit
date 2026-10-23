Contributing
============

To contribute to Django Suit::

    # Clone forked Django Suit repo
    git clone git@github.com:YOUR_USERNAME/django-suit.git suit

    # Install Django Suit from local fork in editable mode
    pip install -e suit

If you wish to participate in development discussions, join our IRC channel ``#django-suit`` on ``irc.freenode.net``

Tests
-----

When contributing don't forget to test your code by running::

    ./manage.py test suit.tests

CSS
---

``suit/static/suit/css/suit.css`` is plain CSS on top of Bootstrap 5, edit it directly. Bootstrap and Bootstrap Icons are vendored, unmodified apart from the removed source map comments, in ``suit/static/suit/bootstrap`` and ``suit/static/suit/bootstrap-icons``.


Related packages
----------------

Related packages you can contribute to:

* `django-suit-redactor <https://github.com/darklow/django-suit-redactor>`_ - Imperavi Redactor (WYSIWYG editor) integration app
* `django-suit-ckeditor <https://github.com/darklow/django-suit-ckeditor>`_ - CKEditor (WYSIWYG editor) integration app
* `django-suit-rq <https://github.com/gsmke/django-suit-rq>`_ - Django-RQ (Queuing library) integration app
* `django-suit-examples <https://github.com/darklow/django-suit-examples>`_ - demo app
