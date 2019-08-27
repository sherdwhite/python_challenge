"""
WSGI config for PythonChallengeApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/Sherd/Documents/Django/Engineering')
sys.path.append('C:/Python/Lib/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)