from django.db import models
from djmoney.models.fields import MoneyField


class Fund(models.Model):
    """
    def __str__(self):
        return self.fund_name
    """
    SOFChoices = [("local", "Local"), ("state", "State"), ("federal", "Federal")]
    fund_id = models.SmallIntegerField(blank=True, primary_key=True)
    fund_name = models.CharField(max_length=255, blank=True)
    fund_cash_balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    #fund_cash_balance = models.TextField(blank=True)  # This field type is a guess.
    dept_id = models.SmallIntegerField(blank=True)
    sof = models.CharField(max_length = 255, blank=True, choices=SOFChoices)
    #sof = models.TextField(blank=True)  # This field type is a guess.
    mac_elig = models.BooleanField(blank=True)

    class Meta:
        db_table = "FUNDS"






