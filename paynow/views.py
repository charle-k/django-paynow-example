import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from .models import *
from .forms import *
from .utils import *


@login_required
def index(request):
    form = MobilePaymentForm()
    confirmed = []
    unconfirmed = []
    payments = PaynowPayment.objects.filter(
             paid=True, user=request.user).order_by('-creation')[:10]
    for payment in payments:
        confirmed.append(payment)

    payments = PaynowPayment.objects.filter(
            paid=False, user=request.user).order_by('-creation')[:10]
    for payment in payments:
        unconfirmed.append(payment)
    return render(request, 'paynow/index.html', {'form': form,
                'confirmed': confirmed, 'unconfirmed': unconfirmed})


@login_required
def my_profile(request):
    return render(request, 'paynow/my_profile.html')


@login_required
def paynow_payment(request):
    """
    This is the functions that initiates the payment process. This is
    where the magic starts
    """
    if request.method == 'POST':
        form = MobilePaymentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Generate unique Transaction ID
            transaction_id = generate_transaction_id()
            pinfo = dict()
            # Generate Urls to pass to Paynow. These are generated dynamicaly
            # and are absolute
            r = reverse('paynow:paynow_update', args=(transaction_id, ))
            pinfo['resulturl'] = request.build_absolute_uri(r)
            r = reverse('paynow:paynow_return', args=(transaction_id,))
            pinfo['returnurl'] = request.build_absolute_uri(r)
            # Payment amount
            pinfo['amount'] = str(cleaned_data['amount'])
            # Payment reference
            pinfo['reference'] = transaction_id
            # refer to the project settin
            pinfo['id'] = str(settings.PAYNOW_INTEGRATION_ID)
            pinfo['additionalinfo'] = 'Payment from '
            pinfo['additionalinfo'] += str(cleaned_data['cellphone'])
            if cleaned_data['reference'] != '':
                pinfo['additionalinfo'] += ' - ' + cleaned_data['reference']
            # authemail can be blank. If set it is used in the login in
            # process on paynow
            pinfo['authemail'] = ''
            pinfo['status'] = 'Message'
            # Create the necessary query string using function
            query_string = paynow_create_url_query(pinfo,
                                            settings.PAYNOW_INTEGRATION_KEY)
            # do a request
            paynow_request = urllib.request.Request(settings.PAYNOW_INIT_URL)
            result = urllib.request.urlopen(paynow_request, query_string)
            result = result.read().decode('utf-8')

            if check_initiate_response(result, settings.PAYNOW_INTEGRATION_KEY):
                resp = parse_paynow_message(result)
                # save payment to database, and record as unpaid
                payment = PaynowPayment(user=request.user,
                                status='unpaid',
                                cellphone=str(cleaned_data['cellphone']),
                                reference=pinfo['reference'],
                                amount=cleaned_data['amount'],
                                additionalinfo=cleaned_data['reference'],
                                authemail=pinfo['authemail'],
                                init_status=resp['status'],
                                pollurl=resp['pollurl'],
                                browserurl=resp['browserurl']
                                )
                payment.save()
                # redirect browser to paynow site for payment
                return redirect(resp['browserurl'], permanent=True)
            else:
                msg = 'Error in processing payment. Please try again'
                messages.error(request, msg)
    else:
        form = MobilePaymentForm()
    # if not POST request or error in inputs return input form
    return render(request, 'paynow/paynow_payment.html',
                    {'form': form})


def paynow_return(request, order_id):
    """This the point where Paynow returns user to our site"""
    uorder = get_object_or_404(PaynowPayment, reference=order_id)
    if uorder.status != 'paid':
        # Check the status of the payment
        t = paynow_check_update(uorder, settings.PAYNOW_INTEGRATION_KEY)
        if t == 'paid':
            msg = "Payment of " + str(uorder.amount) + ' by ' + uorder.cellphone
            msg += " confirmed. Details: " + uorder.additionalinfo
            messages.success(request, msg)
        elif t == 'unpaid':
            msg = "No Confirmation of Payment of "
            msg += str(uorder.amount) + ' by ' + uorder.cellphone
            print(msg)
            messages.error(request, msg)

    return redirect(reverse('index'))


def paynow_update(request, order_id):
    """This the point which Paynow polls our site with a payment status. Its
    a good idea to also poll Paynow manually just in case. I also poll it
    when user is returned to site"""
    uorder = get_object_or_404(PaynowPayment, reference=order_id)
    t = paynow_check_update(uorder, settings.PAYNOW_INTEGRATION_KEY)
    return HttpResponse(t)


@login_required
def confirmed_payments(request):
    payments = PaynowPayment.objects.filter(paid=True).order_by('-creation')
    return render(request, 'paynow/confirmed_payments.html',
                    {'payments': payments})


@login_required
def unconfirmed_payments(request):
    payments = PaynowPayment.objects.filter(paid=False).order_by('-creation')
    return render(request, 'paynow/unconfirmed_payments.html',
                    {'payments': payments})


def logout_user(request):
    logout(request)
    msg = 'You have successfully logged out, Hope to see you back soon.'
    messages.success(request, msg)
    return redirect('login')
