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
DECIMAL_PLACES_PRICE = 4
# To store value up to 10 000 000 EUR:
MAX_DIGITS_EUR = 9
MAX_DIGITS_BTC = 11
MAX_DIGITS_LTC = 14
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

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)

class Withdrawal_eur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    iban = models.CharField(max_length=42)
    is_pending = models.BooleanField(default=True)

class Withdrawal_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    address = models.CharField(max_length=100)
    is_pending = models.BooleanField(default=True)

class Withdrawal_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    time_processed = models.DateTimeField(null=True)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    address = models.CharField(max_length=100)
    is_pending = models.BooleanField(default=True)

class Buy_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Sell_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Buy_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Sell_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)

class Deposit_eur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vs = models.CharField(max_length=10)
    eur = models.DecimalField(max_digits=MAX_DIGITS_EUR, decimal_places=DECIMAL_PLACES_EUR)
    datetime = models.DateTimeField()

class Deposit_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    datetime = models.DateTimeField()

class Deposit_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    datetime = models.DateTimeField()

class Order_buy_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Order_sell_btc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    btc = models.DecimalField(max_digits=MAX_DIGITS_BTC, decimal_places=DECIMAL_PLACES_BTC)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Order_buy_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

class Order_sell_ltc(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ltc = models.DecimalField(max_digits=MAX_DIGITS_LTC, decimal_places=DECIMAL_PLACES_LTC)
    price = models.DecimalField(max_digits=MAX_DIGITS_PRICE, decimal_places=DECIMAL_PLACES_PRICE)
    datetime = models.DateTimeField()

 
