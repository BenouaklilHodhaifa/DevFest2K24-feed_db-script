"""
WSGI config for kpi_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kpi_server.settings")

application = get_wsgi_application()

from django.core.management import call_command
import threading

def start_feed_data_script():
    call_command('start_script')

script_thread = threading.Thread(target=start_feed_data_script)
script_thread.start()
