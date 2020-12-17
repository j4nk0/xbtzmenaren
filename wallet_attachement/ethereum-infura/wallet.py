import pickle
from eth_account import Account

# init:
#a = Account.create('RANDOMtgeahgwrpwe9hatgw8oehtgqbue[r-gh[0aeth8eawru')
#priv_keys = { a.address : a.key }
#pickle.dump(priv_keys, open('priv_keys', 'wb'))

priv_keys = pickle.load(open('priv_keys', 'rb'))
print(priv_keys)
