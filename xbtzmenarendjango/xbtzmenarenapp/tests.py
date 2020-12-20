from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal as D

from .models import CustomUser
from .models import Address, Balance

# Create your tests here.
def create_admin():
    password = 'SuperSecret'
    superuser = CustomUser.objects.create_superuser(email='super@Ema.il', password=password)
    superuser.is_verified = True
    superuser.save()
    return superuser.email, password
    
def create_user(email):
    user = CustomUser.objects.create_user(email=email, password='secret1234')
    Address.objects.create(
        user=user,
        vs=f'{CustomUser.objects.get(email=email).id:010}',
        btc='btc:' + f'{CustomUser.objects.get(email=email).id:06}',
        ltc='ltc:' + f'{CustomUser.objects.get(email=email).id:06}',
        doge='doge:' + f'{CustomUser.objects.get(email=email).id:05}',
    )
    Balance.objects.create(
        user=user,
        eur=0,
        btc=0,
        ltc=0,
        doge=0,
    )
    user.is_verified = True
    user.save()
    return user

class RegistrationTests(TestCase):

    def test_create_user(self):
        user = create_user('new@emai.l')
        self.assertEquals('0000000003', user.address.vs)

class DepositTests(TestCase):

    def test_eur_deposit(self):
        eur = D('50')
        user = create_user('an_email@email.email')
        data = { 
           'vs': user.address.vs,
           'sum_eur': eur,
        }
        admin_name, admin_password = create_admin()
        self.client.login(email=admin_name, password=admin_password)
        self.client.post(reverse('deposit-eur-attempt'), data=data)
        user.refresh_from_db()
        self.assertEquals(user.balance.eur, eur)

