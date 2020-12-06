# xbtzmenaren

## Installing dev environment
```
pip install django      #web framework 
pip install psycopg2    #postgresql driver
pip install requests    #for calls to external API
pip install django-axes #login throttling
pip install schwifty    #IBAN validation
pip install ./coinaddr-master   #BTC, LTC address validation
pip install pycoingecko #coingecko api wrapper
pip install python-bitcoinlib #bitcoin rpc caller
pip install litecoin-requests #litecoin rpc caller
```

## Web server:
### Installation:
```
sudo apt install apache2
sudo apt install apache2-dev
sudo apt-get remove libapache2-mod-python libapache2-mod-wsgi
sudo apt-get install libapache2-mod-wsgi-py3
sudo pip3 install mod_wsgi
```
### Setup:
Copy `xbtzmenaren/xbtzmenarendjango/` to `/var/www/xbtzmenarendjango/`

Create `/var/www/logs`

To file:`/etc/apache2/sites-available$ sudo vim new_config.conf`

insert:
```
<VirtualHost *:80>
    ServerName 127.0.0.1
    ServerAlias localhost

    Alias /static /var/www/xbtzmenarendjango/static/
    WSGIScriptAlias / /var/www/xbtzmenarendjango/xbtzmenarendjango/wsgi.py

    <Directory /var/www/xbtzmenarendjango/>
        Order deny,allow
        Allow from all
    </Directory>

    DocumentRoot /var/www/xbtzmenarendjango/
    
    ErrorLog /var/www/logs/error.log
    CustomLog /var/www/logs/custom.log combined
</VirtualHost>
```

Load the new conf file: `sudo a2ensite new_config.conf`

Restart apache: `systemctl restart apache2`

Check apache status: `systemctl status apache2.service | less`

#### Reinstall dependencies:
```
sudo python -m pip install django      #web framework 
sudo python -m pip install psycopg2    #postgresql driver
sudo python -m pip install requests    #for calls to external API
sudo python -m pip install django-axes #login throttling
sudo python -m pip install schwifty==2020.1.1    #IBAN validation
sudo python -m pip install ~/xbtzmenaren/coinaddr-master   #BTC, LTC address validation
sudo python -m pip install pycoingecko #coingecko api wrapper
sudo python -m pip install python-bitcoinlib #bitcoin.rpc caller
sudo python -m pip install litecoin-requests
```

### Start / stop / restart apache2:
```
systemctl start apache2.service
systemctl stop apache2.service
systemctl restart apache2.service
```

disable default apache page: `sudo a2dissite 000-default.conf`

### Enable SSL:

```
<VirtualHost _default_:443>
        ServerName xbtzmenaren.ddns.net
        ServerAlias localhost

        Alias /static /var/www/xbtzmenarendjango/static/
        WSGIScriptAlias / /var/www/xbtzmenarendjango/xbtzmenarendjango/wsgi.py

        <Directory /var/www/xbtzmenarendjango/>
                Order deny,allow
                Allow from all
        </Directory>

        DocumentRoot /var/www/xbtzmenarendjango/

        ErrorLog /var/www/logs/error.log
        CustomLog /var/www/logs/custom.log combined

        SSLEngine on
        SSLCertificateFile /var/www/xbtzmenarendjango/cert.pem
        SSLCertificateKeyFile /var/www/xbtzmenarendjango/privkey.pem

        SSLCipherSuite HIGH:!aNULL:!MD5
</VirtualHost>

```

then: `systemctl reload apache2`

#### Enable redirect from http -> https

```
<VirtualHost *:80>
        ServerName xbtzmenaren.ddns.net
        Redirect permanent / https://xbtzmenaren.ddns.net/
</VirtualHost>
<VirtualHost _default_:443>
        ServerName xbtzmenaren.ddns.net
        ServerAlias localhost

        Alias /static /var/www/xbtzmenarendjango/static/
        WSGIScriptAlias / /var/www/xbtzmenarendjango/xbtzmenarendjango/wsgi.py

        <Directory /var/www/xbtzmenarendjango/>
                Order deny,allow
                Allow from all
        </Directory>

        DocumentRoot /var/www/xbtzmenarendjango/

        ErrorLog /var/www/logs/error.log
        CustomLog /var/www/logs/custom.log combined

        SSLEngine on
        SSLCertificateFile /var/www/xbtzmenarendjango/cert.pem
        SSLCertificateKeyFile /var/www/xbtzmenarendjango/privkey.pem

        SSLCipherSuite HIGH:!aNULL:!MD5
</VirtualHost>
```
### Fix ...ModuleNotFoundError: No module named 'xbtzmenarendjango'...

Do edit:
`/var/www/xbtzmenarendjango/xbtzmenarendjango/wsgi.py` to contain: `sys.path.append('/var/www/xbtzmenarendjango')`

for example:

```
import os
import sys

sys.path.append('/var/www/xbtzmenarendjango')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbtzmenarendjango.settings')

application = get_wsgi_application()

# j4nk0:
import os
os.chdir('..')
import threading
from xbtzmenarenapp.bitcoin_driver import listen as btc_listen
from xbtzmenarenapp.litecoin_driver import listen as ltc_listen

threading.Thread(target=btc_listen, daemon=True).start()
threading.Thread(target=ltc_listen, daemon=True).start()
```

## Enable file upload:

Add to settings.py:
```
MEDIA_ROOT = '/var/www/xbtzmenarendjango/media/'
MEDIA_URL = 'https://xbtzmenaren.ddns.net/media/'
```
and use this syntax in views.py:`with open('/var/www/xbtzmenarendjango/media/' + email + file_description, 'wb+') as destination:`


## Adding new currency - DOGE:

### Adding models:

to `xbtzmenarendjango/zbtzmenarenapp/models`  add:
```
DECIMAL_PLACES_DOGE = 8
DECIMAL_PLACES_DOGE = 18

class Address(models.Model):
    ...
    doge = models.CharField(max_length=100, unique=True)

class Balance(models.Model):
    ...
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)

class Withdrawal_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    address = models.CharField(max_length=100)
    is_pending = models.BooleanField(default=True)

class Buy_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Sell_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Deposit_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    datetime = models.DateTimeField()

class Order_buy_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Order_sell_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Incoming_doge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    confirmations = models.IntegerField()
    txid = models.CharField(max_length=64)
```
