from django.db import models
from django.contrib.auth.models import User


class PaynowPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cellphone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=100)
    paynow_reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=500, blank=True)

    init_status = models.CharField(max_length=10, blank=True)
    poll_url = models.CharField(max_length=500)
    browser_url = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)
    paid = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username + ' - $' + str(self.amount) + ' - ' + self.status
