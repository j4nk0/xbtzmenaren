"""
WSGI config for xbtzmenarendjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/var/www/xbtzmenarendjango')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbtzmenarendjango.settings')

application = get_wsgi_application()
