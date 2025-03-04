from django.db import models
from djmoney.models.fields import MoneyField


class Fund(models.Model):
    def __str__(self):
        return self.fund_name

    SOFChoices = [("local", "Local"), ("state", "State"), ("federal", "Federal")]
    fund_id = models.SmallIntegerField(blank=True, primary_key=True)
    fund_name = models.CharField(max_length=255, blank=False)
    fund_cash_balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    #fund_cash_balance = models.TextField(blank=True)  # This field type is a guess.
    dept_id = models.SmallIntegerField(blank=False)
    sof = models.CharField(max_length = 255, blank=False, choices=SOFChoices)
    #sof = models.TextField(blank=True)  # This field type is a guess.
    mac_elig = models.BooleanField(blank=False)

    class Meta:
        db_table = "Funds"


class Line(models.Model):
    line_id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fund_year = models.SmallIntegerField(blank=False)
    line_name = models.CharField(max_length=255)
    line_budgeted = MoneyField(max_digits = 10, decimal_places=2, default_currency='USD')
    line_encumbered = MoneyField(max_digits = 10, decimal_places=2, default_currency='USD')
    line_budget_spent = MoneyField(max_digits = 10, decimal_places=2, default_currency='USD')
    line_total_income = MoneyField(max_digits = 10, decimal_places=2, default_currency='USD')
    dept_id = models.SmallIntegerField(blank=False)
    cofund = models.CharField(max_length=3)
    gen_ledger = models.IntegerField(blank=False)
    county_code = models.CharField(max_length = 4)

    class Meta:
        db_table = "Lines"
    
    def __str__(self): 
        return f"{self.fund.fund_id}"
    

class Testing(models.Model):
    testing_name = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "Testing"
