*********************
django CMS Article Drafts
*********************

============
Installation
============

Requirements
============

django CMS Article Drafts requires that you have a django CMS 3.4.3 (or higher) project already running and set up.


To install
==========

Run::

    pip install git+git://github.com/trojjer/djangocms-article-drafts

Add ``djangocms_article_drafts`` to your project's ``INSTALLED_APPS``.

Run::

    python manage.py migrate djangocms_article_drafts

to perform the application's database migrations.
