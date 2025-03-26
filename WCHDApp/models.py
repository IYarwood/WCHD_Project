from django.db import models
from djmoney.models.fields import MoneyField

class FundSource(models.TextChoices):
    FEDERAL = 'FEDERAL'
    STATE = 'STATE'
    LOCAL = 'LOCAL'

#REMINDER TO TAKE OUT null=True and blank=True from all instances of dept once we have a department populated
class Dept(models.Model):
    dept_id = models.SmallIntegerField(primary_key=True, verbose_name="Department")
    dept_name = models.CharField(max_length=255, verbose_name="Department Name")
 
    def __str__(self):
        return self.dept_name

    class Meta:
        db_table = "Departments"

class Fund(models.Model):
    SOFChoices = [("local", "Local"), ("state", "State"), ("federal", "Federal")]
    fund_id = models.SmallIntegerField(blank=True, primary_key=True, verbose_name = "Fund ID")
    fund_name = models.CharField(max_length=255, blank=False, verbose_name= "Fund Name")
    fund_cash_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Fund Cash Balance")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    sof = models.CharField(max_length=10, blank = False, choices=FundSource.choices, verbose_name="Source of Funds")
    mac_elig = models.BooleanField(blank=False, verbose_name="Medicaid Administrative Claiming Eligibility")
 
    @property
    def fundBalanceMinus3(self):
        return self.fund_cash_balance - 3
    
    def __str__(self):
        return self.fund_name
    
    class Meta:
        db_table = "Funds"


class Line(models.Model):
    line_id = models.AutoField(primary_key=True, verbose_name="Line ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fund_year = models.SmallIntegerField(blank=False, verbose_name="Fund Year")
    line_name = models.CharField(max_length=255, verbose_name="Line Name")
    line_budgeted = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Line Budgeted")
    line_encumbered = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Line Encumbered")
    line_budget_spent = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Line Budget Spent")
    line_total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Line Total Income")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    cofund = models.CharField(max_length=3, verbose_name="CoFund")
    gen_ledger = models.IntegerField(blank=False, verbose_name="General Ledger")
    county_code = models.CharField(max_length = 4, verbose_name="County Code")

    def __str__(self): 
        return self.line_name
    
    class Meta:
        db_table = "Lines"
    
class Item(models.Model):
    item_id = models.AutoField(primary_key=True, verbose_name="Item ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fund_type = models.CharField(max_length=50, choices=FundSource.choices, verbose_name="Fund Type")
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    fund_year = models.IntegerField(verbose_name="Fund Year")
    item_name = models.CharField(max_length=255, verbose_name="Item Name")
    line_item = models.CharField(max_length=255, verbose_name="Line Item")
    category = models.CharField(max_length=50, verbose_name="Category")
    fee_based = models.BooleanField(verbose_name="Fee Based")
    month = models.IntegerField(verbose_name="Month")
 
    def __str__(self):
        return self.item_name
    
    class Meta:
        db_table = "Items"
    
class Employee(models.Model):
    emp_id = models.IntegerField(primary_key=True, verbose_name="Employee ID")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    surname = models.CharField(max_length=255, verbose_name="Surname")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True)
    street_address = models.CharField(max_length=255, verbose_name="Street Address")
    city = models.CharField(max_length=255, verbose_name="City")
    state = models.CharField(max_length=2, verbose_name="State")
    zip_code = models.IntegerField(verbose_name="Zip Code")
    phone = models.CharField(max_length=12, verbose_name="Phone Number")
    dob = models.DateField(verbose_name="Date of Birth")
    ssn = models.CharField(max_length=11, verbose_name="Social Security Number")
    hire_date = models.DateField(verbose_name="Hire Date")
    yos = models.FloatField(verbose_name="Years of Service")
    job_title = models.CharField(max_length=255, verbose_name="Job Title")
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pay Rate")
 
    def __str__(self):
        return f"{self.first_name} {self.surname}"
    
    class Meta:
        db_table = "Employees"

class People(models.Model):  
    name_id = models.AutoField(primary_key=True, verbose_name="Customer/Vendor")
    name = models.CharField(max_length=255, verbose_name="Name") 
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=2, verbose_name="State")
    zip_code = models.CharField(max_length=10, verbose_name="Zip Code")
    phone = models.CharField(max_length=12, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email")
    primary_contact = models.CharField(max_length=255, blank=True, null=True, verbose_name="Primary Contact") 
    ein = models.CharField(max_length=10, blank=True, null=True, verbose_name="EIN")  
    account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Account Number")
 
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Peoples"
 
class Invoice(models.Model):
    invoice_number = models.AutoField(primary_key=True, verbose_name="Invoice Number")
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Invoice Amount")
    description = models.TextField(verbose_name="Description")
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False,verbose_name="Paid")
    void = models.BooleanField(default=False, verbose_name="Void")
 
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.vendor_customer.name}"
    
    class Meta:
        db_table = "Invoices"
 
class PurchaseOrder(models.Model):
    po_num = models.AutoField(primary_key=True, verbose_name="Purchase Order Number")
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    date = models.DateField(verbose_name="Date")
    type = models.CharField(max_length=20, choices=[('Issue', 'Issue'), ('Pay', 'Pay')], verbose_name="Type")
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    warrant = models.CharField(max_length=50, blank=True, null=True, verbose_name="Warrant")  
    prid = models.CharField(max_length=50, blank=True, null=True, verbose_name="Program ID")  
    grli = models.CharField(max_length=50, blank=True, null=True, verbose_name="Grant Line Item")  
    odhafr = models.CharField(max_length=50, blank=True, null=True, verbose_name="Annual Financial Report")
 
    def __str__(self):
        return f"PO {self.po_num} - {self.business.name}"
    
    class Meta:
        db_table = "PurchaseOrders"
 
class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True, verbose_name="Voucher ID")
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    date = models.DateField(verbose_name="Date")
    paid = models.BooleanField(default=False, verbose_name="Paid")
 
    def __str__(self):
        return f"Voucher {self.voucher_id} - {self.vendor.name}"
    
    class Meta:
        db_table = "Vouchers"

class Testing(models.Model):
    testing_name = models.CharField(max_length=200, blank=True)
    fund_year = models.IntegerField(blank=True, null = True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    
    @property
    def fundBalanceMinus3(self):
        return self.fund.fund_cash_balance - 3

    class Meta:
        db_table = "Testing"

