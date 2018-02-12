import time
import urllib.parse
import hashlib
from django.utils import timezone

PS_ERROR = 'Error'
PS_OK = 'Ok'
PS_CREATED_BUT_NOT_PAID = 'created but not paid'
PS_CANCELLED = 'cancelled'
PS_FAILED = 'failed'
PS_PAID = 'paid'
PS_AWAITING_DELIVERY = 'awaiting delivery'
PS_DELIVERED = 'delivered'
PS_AWAITING_REDIRECT = 'awaiting redirect'


def paynow_create_url_query(values, mkey):
    ifields = {}
    for key in list(values.keys()):
        p = values[key]
        ifields[key] = urllib.parse.quote(p)
    ifields['hash'] = urllib.parse.quote(CreateHash(values, mkey))
    fields_string = UrlIfy(ifields)
    return fields_string.encode('utf-8')


def CreateHash(pinfo, mkey):
    hstring = ""
    # To produce the proper hash, the different parts must be in joined in
    # exactly this order. So do not be tempted to loop over the dictionary as
    # it may give you a different hash on different system
    hstring += pinfo['resulturl']
    hstring += pinfo['returnurl']
    hstring += pinfo['reference']
    hstring += pinfo['amount']
    hstring += pinfo['id']
    hstring += pinfo['additionalinfo']
    hstring += pinfo['authemail']
    hstring += pinfo['status']
    # add the key to end
    hstring += mkey

    hash_object = hashlib.sha512(hstring.encode())
    return hash_object.hexdigest().upper()


def UrlIfy(pinfo):
    hstring = 'resulturl' + '=' + pinfo['resulturl'] + '&'
    hstring += 'returnurl' + '=' + pinfo['returnurl'] + '&'
    hstring += 'reference' + '=' + pinfo['reference'] + '&'
    hstring += 'amount' + '=' + pinfo['amount'] + '&'
    hstring += 'id' + '=' + pinfo['id'] + '&'
    hstring += 'additionalinfo' + '=' + pinfo['additionalinfo'] + '&'
    hstring += 'authemail' + '=' + pinfo['authemail'] + '&'
    hstring += 'status' + '=' + pinfo['status'] + '&'
    hstring += 'hash' + '=' + pinfo['hash']
    return hstring


def parse_paynow_message(data):
    res = {}
    parts = data.split('&')
    for part in parts:
        indparts = part.split("=")
        res[indparts[0]] = urllib.parse.unquote(indparts[1])
    return res


def check_initiate_response(res, key):
    parts = parse_paynow_message(res)
    if parts['status'].upper() == 'OK':
        v = parts['status'] + parts['browserurl'] + parts['pollurl']
        v += key
        hash_object = hashlib.sha512(v.encode())
        if hash_object.hexdigest().upper() == parts['hash']:
            return True
        else:
            return False
    else:
        return False


def paynow_check_response(res, key, uorder):
    parts = parse_paynow_message(res)
    paid = False
    # In case there is a '+' in the status string, replace with an space
    parts['status'] = parts['status'].replace('+', ' ')
    p = parts['status'].lower()
    if p == PS_PAID:
        paid = True
    elif p == PS_AWAITING_DELIVERY:
        paid = True
    elif p == PS_DELIVERED:
        paid = True
    else:
        paid = False
    #if paid and decimal(parts['amount'] == uorder.amount:
    if paid:
        v = parts['reference']
        v += parts['paynowreference']
        v += parts['amount']
        v += parts['status']
        v += parts['pollurl']
        v += key
        print(v)
        hash_object = hashlib.sha512((v.encode('utf-8')))
        if hash_object.hexdigest().upper() == parts['hash']:
            return 'paid'
        else:
            return 'unpaid'
    else:
        return 'unpaid'


def generate_transaction_id():
    """
    Generates a unique id which will be used by paynow to refer to the payment
    initiated
    """
    return str(int(time.time() * 1000))


def paynow_check_update(uorder, key):
    requ = urllib.request.Request(uorder.pollurl)
    result = urllib.request.urlopen(requ)
    result = result.read().decode('utf-8')
    t = paynow_check_response(result, key, uorder)
    if  t == 'paid' and uorder.status != 'paid':
        payme = parse_paynow_message(result)
        uorder.status = 'paid'
        uorder.paid = True
        uorder.confirmed_at = timezone.now()
        uorder.paynow_reference = payme['paynowreference']
        uorder.save()
        return "paid"
    else:
        return "unpaid"