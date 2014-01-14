"""
WSGI config for kleeek project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys, site

sys.path.insert(0, os.path.dirname(__file__))

site.addsitedir('/usr/local/lib/python2.7/dist-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'kleeek.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kleeek.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
