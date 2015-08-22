import os
import sys
sys.path = ['/var/www/html/SGP'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'SGP.settings'
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
