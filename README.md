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
pip install python-bitcoinlib #bitcoin.rpc caller
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
```

### Start / stop / restart apache2:
```
systemctl start apache2.service
systemctl stop apache2.service
systemctl restart apache2.service
```
