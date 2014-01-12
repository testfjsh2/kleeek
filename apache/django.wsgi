import os, sys

sys.path.append('/usr/local/lib/python2.7/dist-packages/django')

sys.path.append('/home/fjshadows/WORK/kleeek')

os.environ['DJANGO_SETTINGS_MODULE'] = 'kleeek.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()