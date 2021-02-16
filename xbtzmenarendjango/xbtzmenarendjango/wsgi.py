"""
WSGI config for xbtzmenarendjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbtzmenarendjango.settings')

application = get_wsgi_application()

# j4nk0:
import os
os.chdir('..')
import threading
from xbtzmenarenapp.bitcoin_driver import listen as btc_listen
from xbtzmenarenapp.litecoin_driver import listen_for_tx as ltc_listen_for_tx
from xbtzmenarenapp.litecoin_driver import listen_for_block as ltc_listen_for_block
from xbtzmenarenapp.dogecoin_driver import listen as doge_listen

threading.Thread(target=btc_listen, daemon=True).start()
threading.Thread(target=ltc_listen_for_tx, daemon=True).start()
threading.Thread(target=ltc_listen_for_block, daemon=True).start()
threading.Thread(target=doge_listen, daemon=True).start()
