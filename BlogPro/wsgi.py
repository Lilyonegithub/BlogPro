"""
WSGI config for BlogPro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogPro.settings')
profile = os.environ.get('BLOGPRO_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogPro.setting.%s' %profile)

application = get_wsgi_application()
