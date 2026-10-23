"""
Kept for backwards compatibility with projects and templates that import
from here (e.g. ``{% load url from suit_compat %}``).
In order to avoid circular references, nothing should be imported from suit lib.
"""
from importlib import import_module  # noqa: F401

from django.contrib.contenttypes import admin as ct_admin  # noqa: F401
from django.template.defaulttags import url  # noqa: F401

tpl_context_class = dict
