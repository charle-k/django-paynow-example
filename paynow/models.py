from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PaynowPayment(models.Model):
    user = models.ForeignKey(User)
    cellphone = models.CharField(max_length=100, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    paynow_reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    additionalinfo = models.CharField(max_length=500, blank=True)
    authemail = models.CharField(max_length=100, blank=True)
    init_status = models.CharField(max_length=10, blank=True)
    pollurl = models.CharField(max_length=500, blank=True)
    browserurl = models.CharField(max_length=500, blank=True)
    creation = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, blank=True)
    paid = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username + ' - $' + str(self.amount) + ' - ' + self.status
