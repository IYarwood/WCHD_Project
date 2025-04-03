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
 
    """
    @property
    def fundBalanceMinus3(self):
        return self.fund_cash_balance - 3
    """
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
    employee_id = models.IntegerField(primary_key=True, verbose_name="Employee ID")
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

class ActivityList(models.Model):
    program_id = models.AutoField(primary_key=True, verbose_name="Program ID")
    program = models.CharField(max_length=100, verbose_name="Program")
    odhafr = models.CharField(max_length=10, verbose_name="ODHAFR")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    rev_gen = models.BooleanField(default=False, verbose_name="Revenue Generating")
    active = models.BooleanField(default=True, verbose_name="Active")
    fphs = models.CharField(max_length=20,verbose_name= "Foundational Public Health Service")
 
 
    class Meta:
            db_table = "Activity List"
 
class Payroll(models.Model):
    payroll_id = models.CharField(primary_key=True, max_length=12, verbose_name="Payroll ID")
    beg_date = models.DateField(verbose_name="Beginning Date")
    end_date = models.DateField(verbose_name="End Date")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    activityList = models.ForeignKey(ActivityList, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Hours")
    pay_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Pay Amount")
    vacation_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Vacation Used")
    sick_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Sick Used")
    comp_time_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Comp Time Used")
    other_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Other Hours")
    other_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Other Rate")
    #I will add this as a property
    #pay_rate = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    @property
    def pay_rate(self):
        return self.employee.pay_rate
    
    class Meta:
            db_table = "Payroll"
 
class Grants(models.Model):
    grant_id = models.AutoField(primary_key=True, verbose_name="Grant ID")
    grant_name = models.CharField(max_length=30, verbose_name="Grant Name")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    grant_year = models.PositiveSmallIntegerField(verbose_name="Grant Year")
    cfda = models.CharField(max_length=8, verbose_name="Catalog of Federal Domestic Assistance")
    program_name = models.CharField(max_length=150, verbose_name="Program Name")
    award_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Award Amount")
    pt_no = models.CharField(max_length=8, verbose_name="Pass Through Number")
    active = models.BooleanField(default=True, verbose_name="Active")
    beg_date = models.DateField(verbose_name="Beginning Date")
    end_date = models.DateField(verbose_name="End Date")
    fsid = models.CharField(max_length=10, verbose_name="FSID")
    funder = models.CharField(max_length=50, verbose_name="Funder")
 
    class Meta:
            db_table = "Grants"

class BudgetActions(models.Model):
    ba_id = models.AutoField(primary_key=True, verbose_name="Budget Action ID")
    ba_date = models.DateField(verbose_name="Budget Action Date")
    fssf_from = models.CharField(max_length=20, verbose_name="FSSF From") #may want foreign key: line_id from Lines later
    fssf_to = models.CharField(max_length=20, verbose_name="FSSF To")  #same as fssf_from
    comment = models.CharField(max_length=255, verbose_name="Comment")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    approved = models.BooleanField(default=False, verbose_name="Approved")

    #Had to change, cant have 2 auto fields ig
    fs_res_no = models.IntegerField(verbose_name="FS Res Number") #field type might change
 
    class Meta:
        db_table = "Budget Actions"
 
class Carryover(models.Model):
    co_id = models.AutoField(primary_key=True, verbose_name="Carryover ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    fy = models.IntegerField(verbose_name="Fiscal Year") #fiscal year, max length 4
    co_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Carryover Amount")
    encumbered = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Encumbered")
    year_end_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Year-End Balance")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    beg_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Beginning Balance")
    fy_beg_date = models.DateField(verbose_name="Fiscal Year Beginning Date")
    fy_end_date = models.DateField(verbose_name="Fiscal Year End Date")
 
    class Meta:
            db_table = "Carryover"
 
class HealthInsurance(models.TextChoices):
    single = 'Single'
    waived = 'Waived'
    emp_spouse = 'Emp-Spouse'
    emp_child = 'Emp-Child'
    family = 'Family'
 
class LifeInsurance(models.TextChoices):
    ineligible = 'Ineligible'
    rate1 = 'Rate 1'
    rate2 = 'Rate 2'
 
class Benefits(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hrs_per_pay = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Hours Per Pay")
    #pers = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Public Employee Retirement System")
    #medicare = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Medicare")
    #wc = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Workman's Compensation")
    vac_elig = models.BooleanField(default=True, verbose_name="Vacation Eligible") #not sure on default
    #vacation = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Vacation")
    #plar = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Paid Leave Accumulation Rate")  
    #sick = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Sick Leave")
    #holiday = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Holiday Hours")
    #total_hrly = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Total Hourly")
    #percent_leave = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Percent Leave")
    #monthly_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Monthly Hours")
    ins_type = models.CharField(max_length=10, choices=HealthInsurance.choices, verbose_name="Insurance Type")
    board_ins_share = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Board Insurance Share")
    #board_share_hrly = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Board Share Hourly")
    life_rate = models.CharField(max_length=10, choices=LifeInsurance.choices, verbose_name="Life Insurance Rate")
    #life_hrly = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Life Hourly")
    #salary = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Salary")
    #fringe = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Fringe")
    #total_comp = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Compensation")
 
    @property
    def pers(self):
        value = round((float(self.employee.pay_rate) * 0.14), 2)
        return f"{value:.2f}"
    
    @property
    def medicare(self):
        value = round(float(self.employee.pay_rate) * 0.0145,2)
        return f"{value:.2f}"
    
    #CHECK WHERE TO GET HOURS FROM
    @property
    def wc(self):
        value = round(0.22/float(self.hrs_per_pay),2)
        return f"{value:.2f}"

    @property
    def plar(self):
        yos = self.employee.yos
        factor = 0.03875
        if yos >= 8 and yos < 15:
            factor = 0.0575
        elif yos >= 15 and yos < 25:
            factor = 0.0775
        elif yos >=25:
            factor = 0.096
        value = round(float(yos) * factor,2)
        return f"{value:.2f}"

    @property
    def vacation(self):
        if self.vac_elig:
            value = round(float(self.plar) * float(self.employee.pay_rate), 2)
        else:
            value = 0
        return f"{value:.2f}"
    
    #CHECK THIS IS WHAT IS MEANT
    @property
    def sick(self):
        value = round(float(self.employee.pay_rate) * 0.0575,2)
        return f"{value:.2f}"

    @property
    def holiday (self):
        value = round((96*(float(self.employee.pay_rate)+ float(self.pers) + float(self.medicare) + float(self.wc)))  / (float(self.hrs_per_pay)*26), 2)
        return f"{value:.2f}"

    @property
    def total_hrly(self):
        value = float(self.employee.pay_rate) + float(self.pers) + float(self.medicare) + float(self.wc) + float(self.vacation) + float(self.sick) + float(self.holiday)
        return f"{value:.2f}"

    @property
    def percent_leave(self):
        value = ((float(self.vacation) + float(self.sick) + float(self.holiday))/float(self.total_hrly))* float(100)
        return f"{value:.2f}"
    
    @property
    def monthly_hours(self):
        value = round(float(self.hrs_per_pay) * 4, 2)
        return f"{value:.2f}"
    
    @property
    def board_share_hrly(self):
        if float(self.monthly_hours) > 0 :
            value = round(float(self.board_ins_share) / float(self.monthly_hours),2)
        else:
            value = 0
        return f"{value:.2f}"
    
    @property
    def life_hourly(self):
        rate = self.life_rate
        if rate == LifeInsurance.ineligible:
            factor = 0
        elif rate == LifeInsurance.rate1:
            factor = 3.42
        elif rate == LifeInsurance.rate2:
            factor = 1.71
        
        value = float(factor)/float(self.monthly_hours)
        return f"{value:.2f}"
    
    @property
    def salary(self):
        value = round(float(self.employee.pay_rate) * float(self.hrs_per_pay),2)
        return f"{value:.2f}"
    
    @property
    def fringes(self):
        value = round(((float(self.pers) + float(self.medicare))*float(self.hrs_per_pay)*26) + (float(self.board_ins_share)*12),2)
        return f"{value:.2f}"
    
    @property
    def total_comp(self):
        value = round(float(self.salary) + float(self.fringes), 2)
        return f"{value:.2f}"
    
    class Meta:
            db_table = "Benefits"
 

class transactionType(models.TextChoices):
    revenue = "Revenue"
    expense = "Expense"
class paymentType(models.TextChoices):
    cash = "Cash"
    card = "Card"
class Transaction(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Date")
    type = models.CharField(max_length=10, choices=transactionType.choices, verbose_name="Type")
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Amount")
    payType = models.CharField(max_length=10, choices=paymentType.choices, verbose_name="Payment Type")
    comment = models.CharField(max_length = 500, verbose_name="Comment")

    class Meta:
            db_table = "Transactions"


class Testing(models.Model):
    testing_name = models.CharField(max_length=200, blank=True)
    fund_year = models.IntegerField(blank=True, null = True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)

    @property
    def fundBalanceMinus3(self):
        return self.fund.fund_cash_balance - 3

    class Meta:
        db_table = "Testing"

