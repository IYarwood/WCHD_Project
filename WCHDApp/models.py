from django.db import models
from djmoney.models.fields import MoneyField

class FundSource(models.TextChoices):
    FEDERAL = 'FEDERAL'
    STATE = 'STATE'
    LOCAL = 'LOCAL'

#REMINDER TO TAKE OUT null=True and blank=True from all instances of dept once we have a department populated
class Dept(models.Model):
    dept_id = models.SmallIntegerField(primary_key=True)
    dept_name = models.CharField(max_length=255)
 
    def __str__(self):
        return self.dept_name

    class Meta:
        db_table = "Departments"

class Fund(models.Model):
    SOFChoices = [("local", "Local"), ("state", "State"), ("federal", "Federal")]
    fund_id = models.SmallIntegerField(blank=True, primary_key=True)
    fund_name = models.CharField(max_length=255, blank=False)
    fund_cash_balance = models.DecimalField(max_digits=15, decimal_places=2)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    sof = models.CharField(max_length=10, blank = False, choices=FundSource.choices)
    mac_elig = models.BooleanField(blank=False)
 
    def __str__(self):
        return self.fund_name

    class Meta:
        db_table = "Funds"


class Line(models.Model):
    line_id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fund_year = models.SmallIntegerField(blank=False)
    line_name = models.CharField(max_length=255)
    line_budgeted = models.DecimalField(max_digits=15, decimal_places=2)
    line_encumbered = models.DecimalField(max_digits=15, decimal_places=2)
    line_budget_spent = models.DecimalField(max_digits=15, decimal_places=2)
    line_total_income = models.DecimalField(max_digits=15, decimal_places=2)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    cofund = models.CharField(max_length=3)
    gen_ledger = models.IntegerField(blank=False)
    county_code = models.CharField(max_length = 4)

    def __str__(self): 
        return self.line_name
    
    class Meta:
        db_table = "Lines"
    
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fund_type = models.CharField(max_length=50, choices=FundSource.choices)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    fund_year = models.IntegerField()
    item_name = models.CharField(max_length=255)
    line_item = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    fee_based = models.BooleanField()
    month = models.IntegerField()
 
    def __str__(self):
        return self.item_name
    
    class Meta:
        db_table = "Items"
    
class Employee(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()
    phone = models.CharField(max_length=12)
    dob = models.DateField()
    ssn = models.CharField(max_length=11)
    hire_date = models.DateField()
    yos = models.FloatField()
    job_title = models.CharField(max_length=255)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
 
    def __str__(self):
        return f"{self.first_name} {self.surname}"
    
    class Meta:
        db_table = "Employees"

class Testing(models.Model):
    testing_name = models.CharField(max_length=200, blank=True)
    fund_year = models.IntegerField(blank=True, null = True)

    class Meta:
        db_table = "Testing"
