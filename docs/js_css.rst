JavaScript & CSS
================

JavaScript goodies
------------------

Inlines hook
^^^^^^^^^^^^

When working with Django inlines and JavaScript, very often we want to hook/attach to event - when new inline row is added. Django Suit gives us such chance.

Use JavaScript ``Suit.after_inline.register`` to register/attach your function to new inline addition event. It runs on Django's ``formset:added`` event, which you can also listen to directly with ``document.addEventListener('formset:added', ...)``.

.. code-block:: javascript

  $(function () {
      Suit.after_inline.register('my_unique_func_name', function(inline_prefix, row){
          // Your code here
          console.info(inline_prefix)
          console.info(row)
      });
  });


.. _css-goodies:


jQuery
^^^^^^

Django Suit loads the jQuery shipped with Django admin (v3.7.1 on Django 5.2 - 6.1) and exposes it under a custom namespace to avoid collisions between different apps which also provide jQuery. To load a different jQuery, override the ``suit_jquery`` block of ``admin/base.html``.

Bootstrap 5 JavaScript (``bootstrap.bundle.min.js``, including Popper) is loaded on every admin page and available as the global ``bootstrap`` object. It does not depend on jQuery.

To use jQuery from Django Suit package:

.. code-block:: javascript

  // Use Suit.$ instead of $
  Suit.$('.my-selector').addClass('my-class');

  // Or for larger code you can wrap it in following way:
  (function ($) {
      // Here you can use regular $ sign
      $('.my-selector').addClass('my-class');
  }(Suit.$));

  // On document ready example:
  (function ($) {
    $(function () {
        $('.my-selector').addClass('my-class');
    });
  }(Suit.$));


CSS goodies
-----------

`Original <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets>`_ ``collapse`` and ``wide`` fieldset classes are also supported by Django Suit. Usage::

  from django.contrib.admin import ModelAdmin

  class CountryAdmin(admin.ModelAdmin):
      ...
      fieldsets = [
          (None, {'fields': ['name', 'description']}),

          ('Advanced settings', {
              'classes': ('collapse',),  # Specify fieldset classes here
              'fields': ['hidden_checkbox', 'hidden_choice']}),
      ]

.. |collapse| image:: _static/img/collapse.png

* ``collapse`` CSS class makes fieldset collapsable:

  |collapse|

* ``collapse`` fieldsets are rendered as a ``<details>`` element (same as Django admin). Add the ``open`` class too (``'classes': ('collapse', 'open')``) to start expanded. Fieldsets with errors are never collapsed.

* ``wide`` CSS class makes fieldset labels wider

* ``full-width`` CSS class hides field label and makes field controls in full width (useful for wysiwyg editors). Because label will be hidden, this class is intended to use one field per fieldset and fieldset title will be used as field title.

  .. image:: _static/img/full-width.png
     :target: http://djangosuit.com/admin/examples/wysiwygeditor/add/




Theming
-------

``suit/css/suit.css`` is plain CSS (there is no build step anymore). Colors, column widths and radii are CSS custom properties defined on ``:root``, so you can restyle Suit from your own stylesheet::

  /* static/css/my_admin.css, added in the extrastyle block of admin/base_site.html */
  :root {
      --suit-accent: #7a4ab8;
      --suit-accent-dark: #5f3797;
      --suit-accent-1: #a77fd6;
      --suit-accent-2: #7a4ab8;
      --suit-left-width: 220px;
  }

Icons
-----

Suit ships `Bootstrap Icons <https://icons.getbootstrap.com/>`_, use them with ``<i class="bi bi-house"></i>``. The Bootstrap 2 ``icon-*`` class names (e.g. ``icon-lock``) used in older configs and templates are mapped to Bootstrap Icons by ``suit/css/glyphicons-compat.css``, so they keep working.
