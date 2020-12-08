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
pip install dogecoin-python   #dogecoin rpc caller
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
sudo python -m pip install python-bitcoinlib #bitcoin rpc caller
sudo python -m pip install litecoin-requests #litecoin rpc caller
sudo python -m pip install dogecoin-python   #dogecoin rpc caller
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

### Add to Models:

to `xbtzmenarendjango/zbtzmenarenapp/models.py` add:

```
DECIMAL_PLACES_DOGE = 8
MAAX_DIGITS_DOGE = 18

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

### Registering models in admin.py:

```
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'vs', 'btc', 'ltc', 'doge',)
    search_fields = ('vs',)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'eur', 'btc', 'ltc', 'doge',)
    search_fields = ('eur', 'btc', 'ltc', 'doge',)

class Withdrawal_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_created', 'time_processed', 'address', 'doge', 'is_pending')
    search_fields = ('address', 'doge',)
    list_filter = ('is_pending',)

class Buy_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'doge', 'eur',)
    search_fields = ('user', 'doge', 'eur')

class Sell_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'doge', 'eur',)
    search_fields = ('user', 'doge', 'eur')

class Deposit_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'doge', 'datetime',)
    search_fields = ('user', 'address', 'doge', 'datetime',)

class Order_buy_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'doge', 'price', 'datetime',)
    search_fields = ('user', 'doge', 'price', 'datetime',)

class Order_sell_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'doge', 'price', 'datetime',)
    search_fields = ('user', 'doge', 'price', 'datetime',)

class Incoming_dogeAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'doge', 'confirmations', 'txid')
    search_fields = ('user', 'address', 'doge', 'confirmations', 'txid')

admin.site.register(Withdrawal_doge, Withdrawal_dogeAdmin)
admin.site.register(Buy_doge, Buy_dogeAdmin)
admin.site.register(Sell_doge, Sell_dogeAdmin)
admin.site.register(Deposit_doge, Deposit_dogeAdmin)
admin.site.register(Order_buy_doge, Order_buy_dogeAdmin)
admin.site.register(Order_sell_doge, Order_sell_dogeAdmin)
admin.site.register(Incoming_doge, Incoming_dogeAdmin)
```

run `python manage.py makemigrations`
and `python manage.py migrate`

-> migrarion error -> make doge address non-unique -> OK
-> dont forget to make it unique later!

### add to Rates:

```
def rates():
    ...
    try:
        doge_buy = r(Order_sell_doge.objects.all().order_by('price')[0].price)
    except:
        doge_buy = 'X'
    try:
        doge_sell = r(Order_buy_doge.objects.all().order_by('-price')[0].price)
    except:
        doge_sell = 'X'
    ...
         'DOGE-EUR': {
             'buy': doge_buy,
             'sell': doge_sell,
        }
    ...
 
def fee_market_buy_doge(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def preview_market_buy_doge(sum_eur):
    sum_eur = D(sum_eur) - fee_market_buy_doge(sum_eur)
    sum_doge = 0
    for order in Order_sell_doge.objects.all().order_by('price'):
        if order.doge * order.price > sum_eur:
           sum_doge += sum_eur / order.price
           break
        else:
            sum_eur -= order.doge * order.price
            sum_doge += order.doge
    if sum_doge <= 0: return 0
    return r(sum_doge.quantize(D(0.1) ** DECIMAL_PLACES_DOGE))

def market_buy_doge(user, sum_eur):
    sum_eur_before_fees = D(sum_eur)
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(eur=F('eur') - D(sum_eur))
        if bal.eur < 0: raise ValueError('Not enough funds')
        Order_sell_doge.objects.all().select_for_update()
        sum_eur = D(sum_eur) - fee_market_buy_doge(sum_eur)
        sum_doge = 0
        for order in Order_sell_doge.objects.all().order_by('price'):
            if order.doge * order.price >= sum_eur:
                sum_doge += sum_eur / order.price
                order.doge -= sum_eur / order.price 
                order.save()
                if order.doge == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + sum_eur)
                break
            else:
                sum_eur -= order.doge * order.price
                sum_doge += order.doge
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(eur=F('eur') + order.doge * order.price)
        else:
            raise ValueError('Market order too big, not enough sell orders to accomodate')
        bal.update(ltc=F('doge') + D(sum_doge))
        Buy_doge.objects.create(
            user=user,
            datetime=timezone.now(),
            doge=sum_doge,
            eur=sum_eur_before_fees,
        )

def fee_market_sell_doge(sum_eur):
    fee = D(sum_eur) * D(0.02)
    if fee < D(1): fee = D(1)
    if fee > D(sum_eur): fee = D(sum_eur)
    return r(fee.quantize(D(0.1) ** DECIMAL_PLACES_EUR))

def preview_market_sell_doge(sum_doge):
    sum_doge = D(sum_doge)
    sum_eur = 0
    for order in Order_buy_doge.objects.all().order_by('-price'):
        if order.doge > sum_doge:
            sum_eur += sum_doge * order.price
            break
        else:
            sum_doge -= order.doge
            sum_eur += order.doge * order.price
    fee = r(fee_market_sell_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return (fee, sum_eur)

def market_sell_doge(user, sum_doge):
    sum_doge = D(sum_doge)
    original_sum_doge = sum_doge
    bal = Balance.objects.filter(user=user)
    with transaction.atomic():
        bal.update(doge=F('doge') - sum_doge)
        if bal.doge < 0: raise ValueError('Not enough funds')
        Order_buy_doge.objects.all().select_for_update()
        sum_eur = 0
        for order in Order_buy_doge.objects.all().order_by('-price'):
            if order.doge >= sum_doge:
                sum_eur += sum_doge * order.price
                order.doge -= sum_doge
                order.save()
                if order.doge == 0: order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(doge=F('doge') + sum_doge)
                break
            else:
                sum_doge -= order.doge
                sum_eur += order.doge * order.price
                order.delete()
                bal_maker = Balance.objects.filter(user=order.user)
                bal_maker.update(doge=F('doge') + order.doge)
        else:
            raise ValueError('Market order too big, not enough buy orders to accomodate')
        sum_eur -= fee_market_sell_doge(sum_eur)
        bal.update(eur=F('eur') + sum_eur)
        Sell_doge.objects.create(
            user=user,
            datetime=timezone.now(),
            doge=original_sum_doge,
            eur=sum_eur,
        )

def fee_limit_order_buy_doge(sum_eur):
    return D(0)

def preview_limit_order_buy_doge(sum_doge, price_doge):
    sum_eur = sum_doge * price_doge
    fee = r(fee_limit_order_buy_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_buy_doge(user, sum_doge, price_doge):
    try:
        if price_doge >= Order_sell_doge.objects.all().order_by('price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_doge * price_doge
    sum_eur_after_fees = sum_eur - fee_limit_order_buy_doge(sum_eur)
    sum_doge_after_fees = sum_eur_after_fees / price_doge
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(eur=F('eur') - sum_eur)
        if bal[0].eur < 0: raise ValueError
        Order_buy_doge.objects.create(
            user=user,
            doge=sum_doge_after_fees,
            price=price_doge,
            datetime=timezone.now()
        )

def delete_limit_order_buy_doge(order_id):
    order = Order_buy_doge.objects.get(id=order_id)
    bal = Balance.objects.filter(user=order.user)
    sum_eur = order.doge * order.price
    with transaction.atomic():
        order.delete()
        bal.update(eur=F('eur') + sum_eur)

def fee_limit_order_sell_doge(sum_eur):
    return D(0)

def preview_limit_order_sell_doge(sum_doge, price_doge):
    sum_eur = sum_doge * price_doge
    fee = r(fee_limit_order_sell_doge(sum_eur))
    sum_eur -= fee
    sum_eur = r(sum_eur.quantize(D(0.1) ** DECIMAL_PLACES_EUR))
    if sum_eur < 0: sum_eur = 0
    return fee, sum_eur

def limit_order_sell_doge(user, sum_doge, price_doge):
    try:
        if price_doge <= Order_buy_doge.objects.all().order_by('-price')[0].price: raise ValueError
    except IndexError:
        pass
    sum_eur = sum_doge * price_doge
    sum_eur_after_fees = sum_eur - fee_limit_order_sell_doge(sum_eur)
    sum_doge_after_fees = sum_eur_after_fees / price_doge
    with transaction.atomic():
        bal = Balance.objects.filter(user=user)
        bal.update(doge=F('doge') - sum_doge)
        if bal[0].ltc < 0: raise ValueError
        Order_sell_ltc.objects.create(
            user=user,
            doge=sum_doge_after_fees,
            price=price_doge,
            datetime=timezone.now()
        )

```

### add to Views:

```
def buy(request, success=None, active='btc'):
    ...
        ...
        'fee_doge': rates.fee_market_buy_doge(sum_eur),
        'sum_doge': rates.preview_market_buy_doge(sum_eur),
        ...

@user_passes_test(verification_check)
@login_required
def buy_doge(request):
    try:
        sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
        rates.market_buy_doge(request.user, sum_eur)
    except:
        return buy(request, False, 'doge')
    return buy(request, True, 'doge')

def buy_doge_json(request):
    sum_eur = dec(request.POST['sum_eur'], DECIMAL_PLACES_EUR)
    data = {
        'fee': str(rates.fee_market_buy_doge(sum_eur)),
        'doge': str(rates.preview_market_buy_doge(sum_eur)),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

def sell(request, success=None, active='btc'):
    ...
    sum_doge = request.user.balance.doge
    ...
    fee_doge, sum_eur_doge = rates.preview_market_sell_doge(sum_doge)
    ...
        ...
        'fee_doge': fee_doge,
        'sum_eur_doge': sum_eur_doge,
        ...

@user_passes_test(verification_check)
@login_required
def sell_doge(request):
    try:
        sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
        rates.market_sell_doge(request.user, sum_doge)
    except:
        return sell(request, False, 'doge')
    return sell(request, True, 'doge')

def sell_doge_json(request):
    sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
    fee, sum_eur = rates.preview_market_sell_doge(sum_doge)
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

def limit_order_buy(request, success=None, active='btc'):
    ...
        ...
        'orders_doge': Order_buy_doge.objects.filter(user=request.user),
        ...

@user_passes_test(verification_check)
@login_required
def limit_order_buy_doge(request):
    try:
        sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
        price_doge = dec(request.POST['price_doge'], DECIMAL_PLACES_PRICE)
        rates.limit_order_buy_doge(request.user, sum_doge, price_doge)
    except:
        return limit_order_buy(request, False, 'doge')
    return limit_order_buy(request, True, 'doge')

@user_passes_test(verification_check)
@login_required
def limit_order_buy_doge_json(request):
    sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
    price_doge = dec(request.POST['price_doge'], DECIMAL_PLACES_PRICE)
    fee, sum_eur = rates.preview_limit_order_buy_doge(sum_doge, price_doge)
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@user_passes_test(verification_check)
@login_required
def limit_order_buy_doge_delete(request, order_id):
    if request.user != Order_buy_doge.objects.get(id=order_id).user:
        return limit_order_buy(request, False, 'doge')
    try:
        rates.delete_limit_order_buy_doge(order_id)
    except:
        return limit_order_buy(request, False, 'doge')
    return limit_order_buy(request, True, 'doge')

def limit_order_sell(request, success=None, active='btc'):
    ...
        ...
        'max_sum_doge': request.user.balance.doge,
        'orders_doge': Order_sell_doge.objects.filter(user=request.user),
        ...

@user_passes_test(verification_check)
@login_required
def limit_order_sell_doge(request):
    try:
        sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
        price_doge = dec(request.POST['price_doge'], DECIMAL_PLACES_PRICE)
        rates.limit_order_sell_doge(request.user, sum_doge, price_doge)
    except:
        return limit_order_sell(request, False, 'doge')
    return limit_order_sell(request, True, 'doge')

def limit_order_sell_doge_json(request):
    sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
    price_doge = dec(request.POST['price_doge'], DECIMAL_PLACES_PRICE)
    fee, sum_eur = rates.preview_limit_order_sell_doge(sum_doge, price_doge)
    data = {
        'fee': str(fee),
        'eur': str(sum_eur),
    }
    res = HttpResponse(json.dumps(data))
    res['Content-Type'] = 'application/json'
    return res

@user_passes_test(verification_check)
@login_required
def limit_order_sell_doge_delete(request, order_id):
    if request.user != Order_sell_doge.objects.get(id=order_id).user:
        return limit_order_buy(request, False, 'doge')
    try:
        rates.delete_limit_order_sell_ltc(order_id)
    except:
        return limit_order_sell(request, False, 'doge')
    return limit_order_sell(request, True, 'doge')

def private_rates(request):
    ...
        ...
        'dogeeur_buy': rates.rates()['DOGE-EUR']['buy'],
        'dogeeur_sell': rates.rates()['DOGE-EUR']['sell'],


def public_rates(request):
    ...
        ...
        'dogeeur_buy': rates.rates()['DOGE-EUR']['buy'],
        'dogeeur_sell': rates.rates()['DOGE-EUR']['sell'],
        ...


def rates_json(request):
    ...
    data['DOGE-EUR']['buy'] = str(data['DOGE-EUR']['buy'])
    data['DOGE-EUR']['sell'] = str(data['DOGE-EUR']['sell'])
    ...

def registration_attempt(request):
    ...
        ...
            ...
            doge=dogecoin_driver.get_new_address(),
            ...
            doge=0,
            ...

def portfolio(request):
    ...
    doge_in_orders = Order_sell_doge.objects.filter(user=request.user).aggregate(Sum('doge'))['doge__sum']
    if doge_in_orders == None: doge_in_orders = D(0)
    ...
        ...
        'doge': rates.r(request.user.balance.doge),
        ...
        'doge_in_orders': rates.r(doge_in_orders),
        ...

def deposit(request):
    ...
        ...
        'doge_address': request.user.address.doge,
        ...
        'incoming_doge': Incoming_doge.objects.filter(user=request.user),


def withdrawal(request, error_message=None, ok_message=None, active='eur'):
    ...
        ...
        'max_sum_doge': request.user.balance.doge - dogecoin_driver.get_fee_per_kB(),

@user_passes_test(verification_check)
@login_required
def withdrawal_doge(request):
    try:
        sum_doge = dec(request.POST['sum_doge'], DECIMAL_PLACES_DOGE)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='doge')
    address_doge = request.POST['address_doge']
    if not is_valid_doge_address(address_doge):
        return withdrawal(request, error_message='Nesprávna adresa', active='doge')
    try:
        with transaction.atomic():
            fee = dogecoin_driver.get_fee_per_kB()
            balance = Balance.objects.filter(user=request.user)
            balance.update(doge=F('doge') - (sum_doge + fee))
            if balance[0].doge < 0: raise ValueError
            if dogecoin_driver.get_balance() < (sum_doge + fee):
                Withdrawal_doge.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    doge=sum_doge,
                    address=address_doge,
                    is_pending=True,
                )
            else:
                Withdrawal_doge.objects.create(
                    user=request.user,
                    time_created=timezone.now(),
                    time_processed=timezone.now(),
                    ltc=sum_doge,
                    address=address_doge,
                    is_pending=False,
                )
                dogecoin_driver.send(address_doge, sum_doge, fee)
    except ValueError:
        return withdrawal(request, error_message='Nesprávna hodnota', active='doge')
    return withdrawal(request, ok_message='Požiadavka zaregistrovaná', active='doge')

def management_withdrawals(request, active='eur'):
    ...
        ...
        'old_withdrawals_doge': Withdrawal_doge.objects.filter(is_pending=False).order_by('-time_processed')[:5],
        ...
        'withdrawals_doge': Withdrawal_doge.objects.filter(is_pending=True).order_by('address')[:100],
        ...

@user_passes_test(verification_check)
@user_passes_test(staff_check)
@login_required 
def management_withdrawal_doge_check(request, withdrawal_id):
    withdrawal = Withdrawal_doge.objects.get(id=withdrawal_id)
    withdrawal.is_pending = False
    withdrawal.time_processed=timezone.now()
    withdrawal.save()
    return management_withdrawals(request, 'doge')

def management_balances(request):
    ...
    orders = Order_buy_doge.objects.filter(user=request.user)
    for o in orders:
        if o.user in staff:
            eur_in_orders_staff += o.doge * o.price
        else:
            eur_in_orders_non_staff += o.doge * o.price
    ... 
    doge_in_orders_staff = D(0)
    doge_in_orders_non_staff = D(0)
    for user in CustomUser.objects.all():
        if user in staff:
            amount = Order_sell_doge.objects.filter(user=user).aggregate(Sum('doge'))['doge__sum']
            if amount: doge_in_orders_staff += amount
        else:
            amount = Order_sell_doge.objects.filter(user=user).aggregate(Sum('doge'))['doge__sum']
            if amount: doge_in_orders_non_staff += amount
    ...
    total_doge = Balance.objects.aggregate(Sum('doge'))['doge__sum']
    ...
    staff_doge = D(0)
    ...
        ...
        staff_doge += user.balance.doge
    ...
    non_staff_doge = total_doge - staff_doge
    ...
        ...
        'doge_in_orders_staff': rates.r(doge_in_orders_staff),
        'doge_in_orders_non_staff': rates.r(doge_in_orders_non_staff),
        'doge_in_orders_total': rates.r(doge_in_orders_staff + doge_in_orders_non_staff),
        ...
        'non_staff_doge': rates.r(non_staff_doge),
        'staff_doge': rates.r(staff_doge),
        'total_doge': rates.r(total_doge),

def management_buys(request):
    ...
        ...
        'buys_doge': Buy_doge.objects.all().order_by('-datetime')[:100],

def management_sells(request):
    ...
        ...
        'sells_doge': Sell_doge.objects.all().order_by('-datetime')[:100],


def management_orderbook(request):
    ...
        ...
        'buy_doge': Order_buy_doge.objects.all().order_by('-price')[:100:-1],
        'sell_doge': Order_sell_doge.objects.all().order_by('price')[:100],
```

### add to templates:

#### buy.html:

```
      ...
      {% if active == "doge" %}
        <li class="active" >
      {% else %}
        <li>
      {% endif %}
          <a data-toggle="pill" href="#Dogecoin">Dogecoin</a>
        </li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <form action="{% url 'buy-doge' %}" method="post">
          {% csrf_token %}
          <div class="form-group">
            <label for="usr">Nakúpiť za EUR:</label>
            <input id="sum_eur_doge" type="text" class="form-control" name="sum_eur"/>
          </div>
          <div>Poplatky: <b id="fee_doge">{{ fee_doge }}</b> EUR</div>
          <div>Nákup: <b>~</b><b id="sum_doge">{{ sum_doge }}</b> DOGE</div>
          <button type="submit" class="btn btn-default">Kúpiť</button>
        </form>
      </div>
      ...
    $('#sum_eur_doge').on("change paste keyup", function() {
      if(isNaN($('#sum_eur_doge').val()) 
        || $('#sum_eur_doge').val() == ""
        || $('#sum_eur_doge').val() == 0) 
      {
        $('#sum_doge').text("-");
        $('#fee_doge').text("-");
      };
      $.post("{% url 'buy-doge-json' %}",
        { sum_eur: $('#sum_eur_doge').val(), csrfmiddlewaretoken: '{{ csrf_token }}' },
        function(data) {
          $('#sum_doge').text(data.doge);
          $('#fee_doge').text(data.fee);
        }
      );
    });
```

#### deposit.html:

```

    ...
      <li><a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
    ...
      <div id="Dogecoin" class="tab-pane">
        <p>Zašlite na adresu:</p>
	<p><b>{{ doge_address }}</b></p>
        <p>Prichádzajúce platby (na pripísanie sumy je treba 6 potvrdení):</p>
        <table class="table">
          <thead>
            <tr>
              <th>Adresa</th>
              <th>Suma DOGE</th>
              <th>Potvrdení</th>
            </tr>
          </thead>
          <tbody>
            {% for incoming in incoming_doge %}
              <tr>
                <td>{{ incoming.address }}</td>
                <td>{{ incoming.doge }}</td>
                <td>{{ incoming.confirmations }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
```

#### limitOrderBuy.html:

```
      ...
      {% if active == "doge" %}
        <li class="active" >
      {% else %}
        <li>
      {% endif %}
          <a data-toggle="pill" href="#Dogecoin">Dogecoin</a>
        </li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <form action="{% url 'limit-order-buy-doge' %}" method="post">
          {% csrf_token %}
          <div>Maximálna celková cena: <b id="max_sum_eur">{{ max_sum_eur }}</b> EUR</div>
          <div class="form-group">
            <label for="usr">Množstvo DOGE:</label>
            <input id="sum_doge" type="text" class="form-control" name="sum_doge"/>
          </div>
          <div class="form-group">
            <label for="usr">Cena DOGE-EUR:</label>
            <input id="price_doge" type="text" class="form-control" name="price_doge"/>
          </div>
          <div>Poplatky: <b id="fee_eur_doge">-</b> EUR</div>
          <div>Celková cena: <b id="sum_eur_doge">-</b> EUR</div>
          <button type="submit" class="btn btn-default">Objednať</button>
        </form>

        <table class="table">
          <thead>
              <tr>
                <td><b>DOGE</b></td>
                <td><b>Cena</b></td>
                <td><b>Čas</b></td>
                <td><b>Zrušiť</b></td>
              </tr>
          </thead>
          <tbody>
            {% for order in orders_doge %}
              <tr>
                <td>{{ order.doge }}</td>
                <td>{{ order.price }}</td>
                <td>{{ order.datetime }}</td>
                <td>
                  <form action="{% url 'limit-order-buy-doge-delete' order.id %}" method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-default">Zrušiť</button>
                  </form>
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
    function onChangeDoge() {
      if(isNaN($('#sum_doge').val()) 
        || $('#sum_doge').val() == ""
        || $('#sum_doge').val() == 0
        || isNaN($('#price_doge').val()) 
        || $('#price_doge').val() == ""
        || $('#price_doge').val() == 0)
      {
        $('#fee_eur_doge').text("-");
        $('#sum_eur_doge').text("-");
      } else {
        $.post("{% url 'limit-order-buy-doge-json' %}",
          { 
            sum_doge: $('#sum_doge').val(),
            price_doge: $('#price_doge').val(),
            csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          function(data) {
            $('#fee_eur_doge').text(data.fee);
            $('#sum_eur_doge').text(data.eur);
          }
        );
      }
    }
    $('#sum_doge').on("change paste keyup", onChangeDoge);
    $('#price_doge').on("change paste keyup", onChangeDoge);
```

#### limitOrderSell.html

```
      ...
      {% if active == "doge" %}
        <li class="active" >
      {% else %}
        <li>
      {% endif %}
          <a data-toggle="pill" href="#Dogecoin">Dogecoin</a>
        </li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <form action="{% url 'limit-order-sell-doge' %}" method="post">
          {% csrf_token %}
          <div>Maximálne množstvo: <b id="max_sum_doge">{{ max_sum_doge }}</b> DOGE</div>
          <div class="form-group">
            <label for="usr">Množstvo DOGE:</label>
            <input id="sum_doge" type="text" class="form-control" name="sum_doge"/>
          </div>
          <div class="form-group">
            <label for="usr">Cena DOGE-EUR:</label>
            <input id="price_doge" type="text" class="form-control" name="price_doge"/>
          </div>
          <div>Poplatky: <b id="fee_eur_doge">-</b> EUR</div>
          <div>Celková cena: <b id="sum_eur_doge">-</b> EUR</div>
          <button type="submit" class="btn btn-default">Objednať</button>
        </form>
        
        <table class="table">
          <thead>
              <tr>
                <td><b>DOGE</b></td>
                <td><b>Cena</b></td>
                <td><b>Čas</b></td>
                <td><b>Zrušiť</b></td>
              </tr>
          </thead>
          <tbody>
            {% for order in orders_doge %}
              <tr>
                <td>{{ order.doge }}</td>
                <td>{{ order.price }}</td>
                <td>{{ order.datetime }}</td>
                <td>
                  <form action="{% url 'limit-order-sell-doge-delete' order.id %}" method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-default">Zrušiť</button>
                  </form>
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
    function onChangeDoge() {
      if(isNaN($('#sum_doge').val()) 
        || $('#sum_doge').val() == ""
        || $('#sum_doge').val() == 0
        || isNaN($('#price_doge').val()) 
        || $('#price_doge').val() == ""
        || $('#price_doge').val() == 0)
      {
        $('#fee_eur_doge').text("-");
        $('#sum_eur_doge').text("-");
      } else {
        $.post("{% url 'limit-order-sell-doge-json' %}",
          { 
            sum_doge: $('#sum_doge').val(),
            price_doge: $('#price_doge').val(),
            csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          function(data) {
            $('#fee_eur_doge').text(data.fee);
            $('#sum_eur_doge').text(data.eur);
          }
        );
      }
    }
    $('#sum_doge').on("change paste keyup", onChangeDoge);
    $('#price_doge').on("change paste keyup", onChangeDoge);
```

#### portfolio.html

```
        ...
        <tr>
          <td><b>{{ doge }}</b></td>
          <td><b>DOGE</b></td>
        </tr>
        ...
         <tr>
          <td><b>{{ doge_in_orders }}</b></td>
          <td><b>DOGE</b></td>
        </tr>
        ...
```

#### privateRates.html and publicRates.html

```
        ...
        <tr>
          <td><b>DOGE-EUR</b></td>
          <td></td>
        </tr>
        <tr>
          <td>Nakúpite za</td>
          <td><b id="dogeeur-buy">{{ dogeeur_buy }}</b></td>
        </tr>
        <tr>
          <td>Predáte za</td>
          <td><b id="dogeeur-sell">{{ dogeeur_sell }}</b></td>
        </tr>
        ...
        $('#dogeeur-buy').text(response["DOGE-EUR"].buy);
        $('#dogeeur-sell').text(response["DOGE-EUR"].sell);
        ...
```
 
#### sell.html

```
      ...
      {% if active == "doge" %}
      <li class="active">
      {% else %}
      <li>
      {% endif %}
      <a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <form action="{% url 'sell-doge' %}" method="post">
          {% csrf_token %}
          <div class="form-group">
            <label for="usr">Predať DOGE:</label>
            <input type="text" class="form-control" name="sum_doge" id="sum_doge"/>
          </div>
          <div>Poplatky: <b id="fee_doge">{{ fee_doge }}</b> EUR</div>
          <div>Predaj za: <b>~</b><b id="sum_eur_doge">{{ sum_eur_doge }}</b> EUR</div>
          <button type="submit" class="btn btn-default">Predať</button>
        </form>
      </div>
      ...
    $('#sum_doge').val('{{ max_sum_doge }}');
    ...
    $('#sum_doge').on("change paste keyup", function() {
      if(isNaN($('#sum_doge').val()) 
        || $('#sum_doge').val() == ""
        || $('#sum_doge').val() == 0)
      {
        $('#sum_eur_doge').text("-");
        $('#fee_doge').text("-");
      };
      $.post("{% url 'sell-doge-json' %}",
        { sum_doge: $('#sum_doge').val(), csrfmiddlewaretoken: '{{ csrf_token }}' },
        function(data) {
          $('#sum_eur_doge').text(data.eur);
          $('#fee_doge').text(data.fee);
        }
      );
    });
    ...
```

#### withdrawal.html

```
      ...
      {% if active == "doge" %}
      <li class="active">
      {% else %}
      <li>
      {% endif %}
      <a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <form action="{% url 'withdrawal-doge' %}" method="post">
          {% csrf_token %}
          <div class="form-group">
            <label for="usr">Vybrať DOGE:</label>
            <input type="text" class="form-control" name="sum_doge" id="sum_doge"/>
            <script>$('#sum_doge').val('{{ max_sum_doge }}');</script>
          </div>
          <div class="form-group">
            <label for="usr">Zaslať na adresu:</label>
            <input type="text" class="form-control"
	      name="address_doge" id="address_doge"/>
          </div>
          <button type="submit" class="btn btn-default">Vybrať</button>
        </form>
      </div>
      ...
```

#### management/balances.html

```
        ...
        <tr>
          <td><b>DOGE</b></td>
          <td>{{ non_staff_doge }}</td>
          <td>{{ staff_doge }}</td>
          <td>{{ total_doge }}</td>
        </tr>
        ...
        <tr>
          <td><b>DOGE</b></td>
          <td>{{ doge_in_orders_non_staff }}</td>
          <td>{{ doge_in_orders_staff }}</td>
          <td>{{ doge_in_orders_total }}</td>
        </tr>
      </tbody>
      ...
```

#### management/buys.html

```
      ...
      <li><a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      <div id="Dogecoin" class="tab-pane">
        <table class="table">
          <thead>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>Čas</b></td>
                <td><b>DOGE</b></td>
                <td><b>EUR</b></td>
              </tr>
          </thead>
          <tbody>
            {% for buy in buys_doge %}
              <tr>
                <td>{{ buy.user }}</td>
                <td>{{ buy.datetime }}</td>
                <td>{{ buy.doge }}</td>
                <td>{{ buy.eur }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
```

#### management/orderbook.html

```
      ...
      <li><a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      <div id="Dogecoin" class="tab-pane">
        <table class="table">
          <thead>
              <tr>
                <td><b>Nákupy<b></td>
              </tr>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>DOGE</b></td>
                <td><b>Cena</b></td>
                <td><b>Čas</b></td>
              </tr>
          </thead>
          <tbody>
            {% for order in buy_doge %}
              <tr>
                <td>{{ order.user }}</td>
                <td>{{ order.doge }}</td>
                <td>{{ order.price }}</td>
                <td>{{ order.datetime }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
        <table class="table">
          <thead>
              <tr>
                <td><b>Predaje<b></td>
              </tr>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>DOGE</b></td>
                <td><b>Cena</b></td>
                <td><b>Čas</b></td>
              </tr>
          </thead>
          <tbody>
            {% for order in sell_doge %}
              <tr>
                <td>{{ order.user }}</td>
                <td>{{ order.doge }}</td>
                <td>{{ order.price }}</td>
                <td>{{ order.datetime }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
```

#### management/sells.html

```
      ...
      <li><a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      <div id="Dogecoin" class="tab-pane">
        <table class="table">
          <thead>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>Čas</b></td>
                <td><b>DOGE</b></td>
                <td><b>EUR</b></td>
              </tr>
          </thead>
          <tbody>
            {% for sell in sells_doge %}
              <tr>
                <td>{{ sell.user }}</td>
                <td>{{ sell.datetime }}</td>
                <td>{{ sell.doge }}</td>
                <td>{{ sell.eur }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
```

#### management/withdrawals.html

```
      ...
      {% if active == "doge" %}
      <li class="active">
      {% else %}
      <li>
      {% endif %}
      <a data-toggle="pill" href="#Dogecoin">Dogecoin</a></li>
      ...
      {% if active == "doge" %}
      <div id="Dogecoin" class="tab-pane active">
      {% else %}
      <div id="Dogecoin" class="tab-pane">
      {% endif %}
        <table class="table">
          <thead>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>Adresa</b></td>
                <td><b>Suma</b></td>
                <td><b>Vytvorené</b></td>
                <td><b>Vybavené</b></td>
              </tr>
          </thead>
          <tbody>
            {% for withdrawal in old_withdrawals_doge %}
              <tr>
                <td>{{ withdrawal.user }}</td>
                <td>{{ withdrawal.address }}</td>
                <td>{{ withdrawal.doge }}</td>
                <td>{{ withdrawal.time_created }}</td>
                <td>{{ withdrawal.time_processed }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
        <table class="table">
          <thead>
              <tr>
                <td><b>Užívateľ</b></td>
                <td><b>Adresa</b></td>
                <td><b>Suma</b></td>
                <td><b>Vytvorené</b></td>
                <td><b>Vybavené</b></td>
              </tr>
          </thead>
          <tbody>
            {% for withdrawal in withdrawals_doge %}
              <tr>
                <td>{{ withdrawal.user }}</td>
                <td>{{ withdrawal.address }}</td>
                <td>{{ withdrawal.doge }}</td>
                <td>{{ withdrawal.time_created }}</td>
                <td>
                  <form action="{% url 'management-withdrawal-doge-check' withdrawal.id %}" method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-default">Vybavené</button>
                  </form>
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      ...
```

### Add to URLS:

```
    ...
    path('buy-doge/', views.buy_doge, name='buy-doge'),
    path('sell-doge/', views.sell_doge, name='sell-doge'),
    path('limit-order-buy-doge/', views.limit_order_buy_doge, name='limit-order-buy-doge'),
    path('limit-order-buy-doge/json', views.limit_order_buy_doge_json, name='limit-order-buy-doge-json'),
    path('limit-order-sell-doge/', views.limit_order_sell_doge, name='limit-order-sell-doge'),
    path('limit-order-sell-doge/json', views.limit_order_sell_doge_json, name='limit-order-sell-doge-json'),
    path('limit-order-buy-doge-delete/<int:order_id>', views.limit_order_buy_doge_delete, name='limit-order-buy-doge-delete'),
    path('limit-order-sell-doge-delete/<int:order_id>', views.limit_order_sell_doge_delete, name='limit-order-sell-doge-delete'),
    path('buy-doge/json', views.buy_doge_json, name='buy-doge-json'),
    path('sell-doge/json', views.sell_doge_json, name='sell-doge-json'),
    path('withdrawal-doge/', views.withdrawal_doge, name='withdrawal-doge'),
    path('management/withdrawal-doge-check/<int:withdrawal_id>', views.management_withdrawal_doge_check, name='management-withdrawal-doge-check'),
    ...
```
