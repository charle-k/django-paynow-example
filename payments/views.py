import time

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

# Import Paynow class
from paynow import Paynow


from .models import PaynowPayment
from .forms import PaymentForm


def generate_transaction_id():
    """
    Generates a unique id which will be used by paynow to refer to the payment
    initiated
    """
    return str(int(time.time() * 1000))

@login_required
def index(request):
    confirmed = []
    unconfirmed = []
    payments = PaynowPayment.objects.filter(
             paid=True, user=request.user).order_by('-created')[:10]
    for payment in payments:
        confirmed.append(payment)

    payments = PaynowPayment.objects.filter(
            paid=False, user=request.user).order_by('-created')[:10]
    for payment in payments:
        unconfirmed.append(payment)
    return render(request, 'payments/index.html', {'confirmed': confirmed, 'unconfirmed': unconfirmed})


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
        form = PaymentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Generate unique Transaction ID
            transaction_id = generate_transaction_id()

            # Generate Urls to pass to Paynow. These are generated dynamicaly
            # and should be absolute
            # result url is used by paynow system to update yo website on the status of a payment
            r = reverse('payments:paynow_update', args=(transaction_id, ))
            result_url = request.build_absolute_uri(r)
            # return url is the url paynow will return the payee to your site
            r = reverse('payments:paynow_return', args=(transaction_id,))
            return_url = request.build_absolute_uri(r)

            # Create an instance of the Paynow class optionally setting the result and return url(s)
            paynow = Paynow(settings.PAYNOW_INTEGRATION_ID,
                            settings.PAYNOW_INTEGRATION_KEY,
                            result_url,
                            return_url,
                            )

            # Create a new payment passing in the reference for that payment(e.g invoice id, or anything that you can
            # use to identify the transaction and the user's email address.
            payment = paynow.create_payment(transaction_id, form.cleaned_data['email'])


            # You can then start adding items to the payment python passing in the name of the item and the price of the
            # item. This is useful when the site has a shopping cart
            payment.add(form.cleaned_data['details'], form.cleaned_data['amount'])

            # When you are finally ready to send your payment to Paynow, you can use the `send` method
            # in the `paynow` object and save the response from paynow in a variable
            response = paynow.send(payment)

            if response.success:
                # Get the link to redirect the user to, then use it as you see fit
                link = response.redirect_url

                # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
                pollUrl = response.poll_url

                # save transaction details to database, and record as unpaid
                payment = PaynowPayment(user=request.user,
                                        status=response.status,
                                        reference=transaction_id,
                                        amount=cleaned_data['amount'],
                                        details=form.cleaned_data['details'],
                                        email=form.cleaned_data['email'],
                                        init_status=response.status,
                                        pollurl=response.poll_url,
                                        browserurl=response.redirect_url,
                                        paynow_reference= response.paynow_reference
                                        )
                payment.save()
                # redirect browser to paynow site for payment
                return redirect(response.redirect_url, permanent=True)
            else:
                msg = 'Error in processing payment. Please try again'
                messages.error(request, msg)
    else:
        form = PaymentForm()
    # if not POST request or error in inputs return input form
    return render(request, 'payments/paynow_payment.html', {'form': form})


def paynow_return(request, payment_id):
    """This the point where Paynow returns user to our site"""
    payment = get_object_or_404(PaynowPayment, reference=payment_id)
    paynow = Paynow(settings.PAYNOW_INTEGRATION_ID, settings.PAYNOW_INTEGRATION_KEY, '', '')

    # Check the status of the payment
    payment_result = paynow.check_transaction_status(payment.poll_url)
    if payment_result.paid:
        if not payment.paid:
            payment.status = payment_result.status
            payment.paid = True
            payment.confirmed_at = timezone.now()
            payment.write()

            msg = "Payment for Transaction " + payment.reference  + ' confirmed'
            msg += " Paynow Reference: " + payment.paynow_reference
            messages.success(request, msg)
            msg = "Payment status => " + payment.status
            messages.success(request, msg)
        else:
            if payment.status != payment_result.status:
                payment.status = payment_result.status
                payment.write()
            msg = "Transaction " + payment.reference + " Payment status => " + payment.status
            messages.success(request, msg)
            msg = "Paynow Reference: " + payment.paynow_reference
            messages.success(request, msg)

    else:
        # Payment has not been paid  yet. So check if payment needs status to be updated
        if payment.status != payment_result.status:
            payment.status = payment_result.status
            payment.write()
        msg = "Transaction " + payment.reference + " Payment status => " + payment.status
        messages.success(request, msg)
        msg = "Paynow Reference: " + payment.paynow_reference
        messages.success(request, msg)

    return redirect(reverse('index'))


def paynow_update(request, payment_reference):
    """This the point which Paynow polls our site with a payment status. I find it best to check with the Paynow Server.
     I also do the check when a payer is returned to the site when user is returned to site"""

    payment = get_object_or_404(PaynowPayment, reference=payment_reference)
    paynow = Paynow(settings.PAYNOW_INTEGRATION_ID, settings.PAYNOW_INTEGRATION_KEY, '', '')
    # Check the status of the payment
    payment_result = paynow.check_transaction_status(payment.poll_url)

    payment_result = paynow.check_transaction_status(payment.poll_url)

    # Check first if paid
    if payment_result.paid:
        if not payment.paid:
            payment.status = payment_result.status
            payment.paid = True
            payment.confirmed_at = timezone.now()
            payment.write()

        else:
            if payment.status != payment_result.status:
                payment.status = payment_result.status
                payment.write()

    else:
        # Payment has not been paid  yet. So check if payment needs status to be updated
        if payment.status != payment_result.status:
            payment.status = payment_result.status
            payment.write()

    return HttpResponse('ok')


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
