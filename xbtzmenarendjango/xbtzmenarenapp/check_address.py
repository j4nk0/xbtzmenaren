import coinaddr

def is_valid_btc_address(address):
    try:
        if coinaddr.validate('btc', address.encode('UTF-8')).valid == True: return True
    except:
        pass
    try:
        if coinaddr.validate('btc-segwit', address.encode('UTF-8')).valid == True: return True
    except:
        pass
    return False

def is_valid_ltc_address(address):
    try:
        if coinaddr.validate('ltc', address.encode('UTF-8')).valid == True: return True
    except:
        pass
    try:
        if coinaddr.validate('ltc-segwit', address.encode('UTF-8')).valid == True: return True
    except:
        pass
    return False
