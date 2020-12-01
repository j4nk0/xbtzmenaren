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
sudo apt install libapache2-mod-wsgi-py3
```
### Setup:
Copy `xbtzmenaren/xbtzmenarendjango/` to `/var/www/xbtzmenarendjango/`
Create `/var/www/logs`

To file:`/etc/apache2/sites-available$ sudo vim new_config.conf`

Insert:
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
restart apache: `systemctl restart apache2`
check apache status: `systemctl status apache2.service | less`

