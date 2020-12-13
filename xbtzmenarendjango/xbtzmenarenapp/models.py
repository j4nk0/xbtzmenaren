from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):

    """Use email instead of username"""
    
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# By design of the systems used:
DECIMAL_PLACES_EUR = 2
DECIMAL_PLACES_BTC = 8
DECIMAL_PLACES_LTC = 8
DECIMAL_PLACES_DOGE = 8
DECIMAL_PLACES_ETH = 18
DECIMAL_PLACES_PRICE = 4
# To store value up to 10 000 000 EUR:
MAX_DIGITS_EUR = 9
MAX_DIGITS_BTC = 11
MAX_DIGITS_LTC = 14
MAX_DIGITS_DOGE = 18
MAX_DIGITS_ETH = 23
MAX_DIGITS_PRICE = 11

class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    vs = models.CharField(max_length=10, unique=True)
    btc = models.CharField(max_length=100, unique=True)
    ltc = models.CharField(max_length=100, unique=True)
    doge = models.CharField(max_length=100, unique=True)
    eth = models.CharField(max_length=100, unique=True)

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    doge = models.DecimalField(max_digits=MAX_DIGITS_DOGE, decimal_places=DECIMAL_PLACES_DOGE)
    eth = models.DecimalField(max_digits=MAX_DIGITS_ETH, decimal_places=DECIMAL_PLACES_ETH)

class Withdrawal_eur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    iban = models.CharField(max_length=42)
    is_pending = models.BooleanField(default=True)

class Deposit_eur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vs = models.CharField(max_length=10)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    datetime = models.DateTimeField()

class Questionare(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    question1 = models.IntegerField()
    question2 = models.IntegerField()
    question3 = models.IntegerField()
    question4 = models.IntegerField()
    question5 = models.IntegerField()
    question6 = models.IntegerField()
    question7 = models.IntegerField()
    question8 = models.IntegerField()
    question9 = models.IntegerField()
    question10 = models.IntegerField()

#======================= Generated code below: =======================#

CURRENCIES = [
    'btc',
    'ltc',
    'doge',
    'eth',
]

DECIMAL_PLACES = {
    'btc': '8',
    'ltc': '8',
    'doge': '8',
    'eth': '18',
}

MAX_DIGITS = {
    'btc': '11',
    'ltc': '14',
    'doge': '18',
    'eth': '23',
}

for c in CURRENCIES:
    exec('''
class Withdrawal_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    address = models.CharField(max_length=100)
    is_pending = models.BooleanField(default=True)

class Buy_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Sell_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Deposit_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    datetime = models.DateTimeField()

class Order_buy_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Order_sell_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Incoming_''' + c + '''(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    ''' + c + ''' = models.DecimalField(max_digits=''' + MAX_DIGITS[c] + ''', decimal_places=''' + DECIMAL_PLACES[c] + ''')
    confirmations = models.IntegerField()
    txid = models.CharField(max_length=64)


''')


