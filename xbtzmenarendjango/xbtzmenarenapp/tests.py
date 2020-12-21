from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal as D

from .models import CustomUser
from .models import Address, Balance
from .models import Order_buy_btc, Sell_btc, Order_sell_btc, Buy_btc
from . import rates

# Create your tests here.

def create_admin():
    '''
    #usage:
    admin_email, admin_password = create_admin()
    self.client.login(email=admin_email, password=admin_password)
    '''
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

class OrderTests(TestCase):
    
    def test_eur_to_btc(self):
        user1 = create_user('user1@user.user')
        user2 = create_user('user2@user.user')
        user1.balance.eur = D('200')
        user1.balance.save()
        user2.balance.btc = D('0.01')
        user2.balance.save()
        self.assertEquals(user1.balance.eur, D('200'))
        self.assertEquals(user2.balance.btc, D('0.01'))
        self.client.logout()
        self.client.force_login(user1)
        data = {
            'sum_btc': D('0.005'),
            'price_btc': D('20000'),
        }
        self.client.post(reverse('limit-order-buy-btc'), data=data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('100'))
        self.assertEquals(user1.balance.btc, D('0'))
        self.assertEquals(user2.balance.eur, D('0'))
        self.assertEquals(user2.balance.btc, D('0.01'))
        order = Order_buy_btc.objects.get(user=user1)
        self.assertEquals(order.btc, D('0.005'))
        self.assertEquals(order.price, D('20000'))
        self.client.logout()
        self.client.login(email=user2.email, password='secret1234')
        data = {
            'sum_btc': D('0.005'),
        }
        fee, sum_eur = rates.preview_market_sell_btc(D('0.005'))
        self.client.post(reverse('sell-btc'), data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        sell_record = Sell_btc.objects.get(user=user2)
        self.assertEquals(sell_record.btc, D('0.005'))
        self.assertEquals(sell_record.eur + fee, D('100'))
        self.assertEquals(user1.balance.eur, D('100'))
        self.assertEquals(user1.balance.btc, D('0.005'))
        self.assertEquals(user2.balance.eur, D('100') - fee)
        self.assertEquals(user2.balance.btc, D('0.005'))

    def test_eur_to_btc_insufficient_funds(self):
        user1 = create_user('user1@user.user')
        user2 = create_user('user2@user.user')
        user1.balance.eur = D('50')
        user1.balance.save()
        user2.balance.btc = D('0.01')
        user2.balance.save()
        self.assertEquals(user1.balance.eur, D('50'))
        self.assertEquals(user2.balance.btc, D('0.01'))
        self.client.logout()
        self.client.force_login(user1)
        data = {
            'sum_btc': D('0.005'),
            'price_btc': D('20000'),
        }
        self.client.post(reverse('limit-order-buy-btc'), data=data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('50'))
        self.assertEquals(user1.balance.btc, D('0'))
        self.assertEquals(user2.balance.eur, D('0'))
        self.assertEquals(user2.balance.btc, D('0.01'))
        self.client.logout()
        self.client.login(email=user2.email, password='secret1234')
        data = {
            'sum_btc': D('0.005'),
        }
        fee, sum_eur = rates.preview_market_sell_btc(D('0.005'))
        self.client.post(reverse('sell-btc'), data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('50'))
        self.assertEquals(user1.balance.btc, D('0'))
        self.assertEquals(user2.balance.eur, D('0'))
        self.assertEquals(user2.balance.btc, D('0.01'))
 
    def test_btc_to_eur(self):
        user1 = create_user('user1@user.user')
        user2 = create_user('user2@user.user')
        user1.balance.btc = D('1')
        user1.balance.save()
        user2.balance.eur = D('500')
        user2.balance.save()
        self.assertEquals(user1.balance.btc, D('1'))
        self.assertEquals(user2.balance.eur, D('500'))
        self.client.logout()
        self.client.force_login(user1)
        data = {
            'sum_btc': D('0.01'),
            'price_btc': D('25000'),
        }
        self.client.post(reverse('limit-order-sell-btc'), data=data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('0'))
        self.assertEquals(user1.balance.btc, D('0.99'))
        self.assertEquals(user2.balance.eur, D('500'))
        self.assertEquals(user2.balance.btc, D('0'))
        order = Order_sell_btc.objects.get(user=user1)
        self.assertEquals(order.btc, D('0.01'))
        self.assertEquals(order.price, D('25000'))
        self.client.logout()
        self.client.force_login(user2)
        data = {
            'sum_eur': D('125'),
        }
        sum_btc = rates.preview_market_buy_btc(D('125'))
        self.assertEquals(sum_btc, D('0.0049'))
        fee = rates.fee_market_buy_btc(D('125'))
        self.client.post(reverse('buy-btc'), data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        buy_record = Buy_btc.objects.get(user=user2)
        self.assertEquals(buy_record.btc, D('0.0049'))
        self.assertEquals(buy_record.eur, D('125'))
        self.assertEquals(fee, D('2.5'))
        self.assertEquals(user1.balance.eur, D('122.5'))
        self.assertEquals(user1.balance.btc, D('0.99'))
        self.assertEquals(user2.balance.eur, D('375'))
        self.assertEquals(user2.balance.btc, D('0.0049'))

    def test_limit_order_buy_btc_delete(self):
        user1 = create_user('user1@user.user')
        user1.balance.eur = D('60')
        user1.balance.save()
        user1.refresh_from_db()
        user1.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('60'))
        self.client.logout()
        self.client.force_login(user1)
        data = {
            'sum_btc': D('0.005'),
            'price_btc': D('10000'),
        }
        self.client.post(reverse('limit-order-buy-btc'), data=data)
        user1.refresh_from_db()
        user1.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('10'))
        self.assertEquals(user1.balance.btc, D('0'))
        order = Order_buy_btc.objects.get(user=user1)
        fee = rates.fee_limit_order_buy_btc(order.btc * order.price)
        self.assertEquals(fee, D('0'))
        self.assertEquals(order.btc + (fee / order.price), D('0.005'))
        self.assertEquals(order.price, D('10000'))
        self.client.post(reverse('limit-order-buy-btc-delete', args=[order.id]))
        user1.refresh_from_db()
        user1.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur + fee, D('60'))
        self.assertEquals(user1.balance.btc, D('0'))
 
    def test_partial_order(self):
        user1 = create_user('user1@user.user')
        user2 = create_user('user2@user.user')
        user3 = create_user('user3@user.user')
        user1.balance.eur = D('1500')
        user1.balance.save()
        user2.balance.btc = D('0.01')
        user2.balance.save()
        user3.balance.btc = D('0.05')
        user3.balance.save()
        self.assertEquals(user1.balance.eur, D('1500'))
        self.assertEquals(user2.balance.btc, D('0.01'))
        self.assertEquals(user3.balance.btc, D('0.05'))
        self.client.logout()
        self.client.force_login(user2)
        data = {
            'sum_btc': D('0.005'),
            'price_btc': D('20000'),
        }
        self.client.post(reverse('limit-order-sell-btc'), data=data)
        self.client.logout()
        self.client.force_login(user3)
        data = {
            'sum_btc': D('0.02'),
            'price_btc': D('25000'),
        }
        self.client.post(reverse('limit-order-sell-btc'), data=data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user3.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        user3.balance.refresh_from_db()
        self.assertEquals(user1.balance.eur, D('1500'))
        self.assertEquals(user1.balance.btc, D('0'))
        self.assertEquals(user2.balance.eur, D('0'))
        self.assertEquals(user2.balance.btc, D('0.005'))
        self.assertEquals(user3.balance.eur, D('0'))
        self.assertEquals(user3.balance.btc, D('0.03'))
        order2 = Order_sell_btc.objects.get(user=user2)
        order3 = Order_sell_btc.objects.get(user=user3)
        self.assertEquals(order2.btc, D('0.005'))
        self.assertEquals(order2.price, D('20000'))
        self.assertEquals(order3.btc, D('0.02'))
        self.assertEquals(order3.price, D('25000'))
        self.client.logout()
        self.client.force_login(user1)
        sum_btc = rates.preview_market_buy_btc(D('300'))
        self.assertEquals(sum_btc, D('0.01276'))
        data = {
            'sum_eur': D('300'),
        }
        self.client.post(reverse('buy-btc'), data)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user3.refresh_from_db()
        user1.balance.refresh_from_db()
        user2.balance.refresh_from_db()
        user3.balance.refresh_from_db()
        self.assertEquals(user1.balance.btc, D('0.01276'))
        self.assertEquals(user1.balance.eur, D('1200'))
        self.assertEquals(user2.balance.eur, D('100'))
        self.assertEquals(user2.balance.btc, D('0.005'))
        self.assertEquals(user3.balance.eur, D('194'))
        self.assertEquals(user3.balance.btc, D('0.03'))
        self.assertRaises(Order_sell_btc.DoesNotExist, Order_sell_btc.objects.get, user=user2)
        order3 = Order_sell_btc.objects.get(user=user3)
        self.assertEquals(order3.btc, D('0.01224'))
        self.assertEquals(order3.price, D('25000'))
        buy_record = Buy_btc.objects.get(user=user1)
        self.assertEquals(buy_record.btc, D('0.01276'))
        self.assertEquals(buy_record.eur, D('300'))

