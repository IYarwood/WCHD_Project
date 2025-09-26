from django.db import models, transaction
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class FundSource(models.TextChoices):
    FEDERAL = 'FEDERAL'
    STATE = 'STATE'
    LOCAL = 'LOCAL'

class Variable(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Variables"


#REMINDER TO TAKE OUT null=True and blank=True from all instances of dept once we have a department populated
class Dept(models.Model):
    dept_id = models.AutoField(primary_key=True, verbose_name="Department ID")
    dept_name = models.CharField(max_length=255, verbose_name="Department Name")
 
    def __str__(self):
        return self.dept_name

    class Meta:
        db_table = "Departments"

class Fund(models.Model):
    SOFChoices = [("local", "Local"), ("state", "State"), ("federal", "Federal")]
    fund_id = models.CharField(max_length=20, primary_key=True, verbose_name = "Fund ID")
    fund_name = models.CharField(max_length=255, blank=False, verbose_name= "Fund Name")
    fund_cash_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Cash Balance")
    fund_total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Given")
    fund_budgeted = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budgeted")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Department")
    sof = models.CharField(max_length=10, blank = False, choices=FundSource.choices, verbose_name="SoF")
    mac_elig = models.BooleanField(blank=False, verbose_name="MACE")

    @property
    def calcRemaining(self):
        lines = self.lines.filter(lineType="Expense")
        total = 0
        for line in lines:
            total += float(line.budgetSpent)
        remaining = float(self.budgeted) - total
        return f"{remaining:.2f}" 
    
    @property
    def budgeted(self):
        lines = self.lines.filter(fund__fund_id=self.fund_id)
        total = 0
        for line in lines:
            total += float(line.line_budgeted)
    
        return f"{total:.2f}" 
    
    @property
    def remainingToBudget(self):
        total = float(self.fund_cash_balance) - float(self.budgeted)
    
        return f"{total:.2f}" 

    def __str__(self):
        return f"({self.fund_id}) {self.fund_name}"
    
    class Meta:
        db_table = "Funds"


class Line(models.Model):
    line_id = models.CharField(primary_key=True, max_length=20, verbose_name="Line ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund", related_name="lines")
    fund_year = models.SmallIntegerField(blank=False, verbose_name="Fund Year")
    line_name = models.CharField(max_length=255, verbose_name="Line Name")
    line_budgeted = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budgeted")
    #line_budget_remaining = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budget Remaining")
    #line_encumbered = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Encumbered")
    #line_budget_spent = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budget Spent", default=0)
    #line_total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Income", default=0)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Department")
    #cofund = models.CharField(max_length=3, verbose_name="CoFund")
    #gen_ledger = models.IntegerField(blank=False, verbose_name="General Ledger")
    #county_code = models.CharField(max_length = 4, verbose_name="County Code")
    lineType = models.CharField(choices=[("Revenue","Revenue"), ("Expense", "Expense")], verbose_name="Line Type")

    @property
    def budgetSpent(self):
        expenses = Expense.objects.filter(line__line_id=self.line_id)
        total = 0
        for expense in expenses:
            total += expense.amount
        
        return f"{total:.2f}"
    
    @property
    def budgetRemaining(self):
        remaining = float(self.line_budgeted) - float(self.budgetSpent)

        return f"{remaining:.2f}"
    
    
    @property
    def totalIncome(self):
        revenues = Revenue.objects.filter(line__line_id = self.line_id)
        total = 0
        for revenue in revenues:
            total += revenue.amount
        
        return f"{total:.2f}"

    def clean(self):
        lines = Line.objects.filter(fund=self.fund)
        total = 0
        for line in lines:
            if line.line_id != self.line_id:
                total += line.line_budgeted
        totalSum = total + self.line_budgeted
       
        if self.fund.fund_total < totalSum:
            raise ValidationError({"line_budgeted":"Not enough remaining balance in fund"})
        
    def save(self, *args, **kwargs):
        #Check if this is the first time calling save on this object
        creating = self._state.adding

        if creating:
            enteredID = self.line_id 
            fundID = self.fund.fund_id 
            fullID = f"{fundID}-{enteredID}"
            self.line_id = fullID


        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
    
    def __str__(self): 
        return self.line_name
    
    class Meta:
        db_table = "Lines"
    
class Item(models.Model):
    item_id = models.AutoField(primary_key=True, verbose_name="Item ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund")
    fund_type = models.CharField(max_length=50, choices=FundSource.choices, verbose_name="Fund Type")
    line = models.ForeignKey(Line, on_delete=models.CASCADE, verbose_name="Line")
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
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Department")
    street_address = models.CharField(max_length=255, verbose_name="Street Address")
    city = models.CharField(max_length=255, verbose_name="City")
    state = models.CharField(max_length=2, verbose_name="State")
    zip_code = models.IntegerField(verbose_name="Zip Code")
    phone = models.CharField(max_length=12, verbose_name="Phone Number")
    dob = models.DateField(verbose_name="DoB")
    ssn = models.CharField(max_length=11, verbose_name="SSN")
    hire_date = models.DateField(verbose_name="Hire Date")
    yos = models.FloatField(verbose_name="YoS")
    job_title = models.CharField(max_length=255, verbose_name="Job Title")
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pay Rate")
    adminPayFund = models.ForeignKey(Fund, on_delete=models.PROTECT, related_name="adminPayFund", verbose_name="Admin Pay Fund")
    specialFund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="special_fund", verbose_name="Special Fund")
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="User account")
    #vac_pay_fund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="vac_pay_fund")
    #sick_pay_fund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="sick_pay_fund")
    #comp_pay_fund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="comp_pay_fund")
    #holiday_pay_fund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="holiday_pay_fund")
    #mac_pay_fund = models.ForeignKey(Fund, on_delete=models.PROTECT,related_name="mac_pay_fund")

    def __str__(self):
        return f"{self.first_name} {self.surname}"
    
    class Meta:
        db_table = "Employees"

class People(models.Model):  
    people_id = models.AutoField(primary_key=True, verbose_name="Customer/Vendor")
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

"""
class Invoice(models.Model):
    invoice_number = models.AutoField(primary_key=True, verbose_name="Invoice Number")
    invoice_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Invoice Amount")
    description = models.TextField(verbose_name="Description")
    people = models.ForeignKey(People, on_delete=models.CASCADE, verbose_name="People")
    date = models.DateField(verbose_name="Date")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False,verbose_name="Paid")
    void = models.BooleanField(default=False, verbose_name="Void")
 
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.vendor_customer.name}"
    
    class Meta:
        db_table = "Invoices"

class PurchaseOrder(models.Model):
    po_num = models.AutoField(primary_key=True, verbose_name="PO Number")
    people = models.ForeignKey(People, on_delete=models.CASCADE, verbose_name="People")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    date = models.DateField(verbose_name="Date")
    type = models.CharField(max_length=20, choices=[('Issue', 'Issue'), ('Pay', 'Pay')], verbose_name="Type")
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    warrant = models.CharField(max_length=50, blank=True, null=True, verbose_name="Warrant")  
    prid = models.CharField(max_length=50, blank=True, null=True, verbose_name="Program ID")  
    grli = models.CharField(max_length=50, blank=True, null=True, verbose_name="GLI")  
    odhafr = models.CharField(max_length=50, blank=True, null=True, verbose_name="ODHAFR")
 
    def __str__(self):
        return f"PO {self.po_num} - {self.business.name}"
    
    class Meta:
        db_table = "PurchaseOrders"

class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True, verbose_name="Voucher ID")
    people = models.ForeignKey(People, on_delete=models.CASCADE, verbose_name="People")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    date = models.DateField(verbose_name="Date")
    paid = models.BooleanField(default=False, verbose_name="Paid")
 
    def __str__(self):
        return f"Voucher {self.voucher_id} - {self.vendor.name}"
    
    class Meta:
        db_table = "Vouchers"
"""
 

class ActivityList(models.Model):
    #Had to change this from program_id
    ActivityList_id = models.AutoField(primary_key=True, verbose_name="Program ID")
    program = models.CharField(max_length=100, verbose_name="Program")
    #odhafr = models.CharField(max_length=10, verbose_name="ODHAFR")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, verbose_name="Department")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund")
    rev_gen = models.BooleanField(default=False, verbose_name="Revenue Generating")
    active = models.BooleanField(default=True, verbose_name="Active")
    fphs = models.CharField(max_length=20,verbose_name= "FPHS")
 
    def __str__(self):
        return self.program

    class Meta:
            db_table = "Activity List"
 
class PayPeriod(models.Model):
    payperiod_id = models.CharField(max_length=7, primary_key=True, verbose_name="Pay Period")
    periodStart = models.DateField(verbose_name="Period Start")
    periodEnd = models.DateField(verbose_name="Periond End")

    def __str__(self):
        return ("Pay Period " + str(self.payperiod_id) + " (" + str(self.periodStart) + " - " + str(self.periodEnd)+")")
    class Meta:
        db_table = "PayPeriod"
 
class Payroll(models.Model):
    id = models.BigAutoField(primary_key=True)
    #payroll_id = models.CharField(primary_key=True, max_length=12, verbose_name="Payroll ID")
    beg_date = models.DateField(max_length=20, verbose_name="Beginning Date")
    end_date = models.DateField(max_length=20, verbose_name="End Date")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    ActivityList = models.ForeignKey(ActivityList, on_delete=models.CASCADE, verbose_name="Activity List")
    #going to get fund from activity list
    #fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Hours")
    pay_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Pay Amount")
    payperiod = models.ForeignKey(PayPeriod, on_delete=models.PROTECT, verbose_name="Pay Period")
    #I think all of these will be properties instead
    #vacation_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Vacation Used")
    #sick_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Sick Used")
    #comp_time_used = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Comp Time Used")
    #other_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Other Hours")
    #other_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Other Rate")
    
    def __str__(self):
        return (str(self.id))

    @property
    def pay_rate(self):
        return self.employee.pay_rate
    
    class Meta:
        db_table = "Payroll"

class Grant(models.Model):
    grant_id = models.AutoField(primary_key=True, verbose_name="Grant ID")
    grant_name = models.CharField(max_length=30, verbose_name="Grant Name")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund")
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
    received = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Received")
    #Used to tell if a grant is allowed more than one revenue lines
    maxRevenueLines = models.IntegerField(default=1)

    @property
    def grantAwardAmountRemaining(self):
        grantLines = GrantLine.objects.filter(grant__grant_id = self.grant_id)
        total = 0
        for line in grantLines:
            total += line.line_budgeted
        totalRemaining = self.award_amount - total
        return totalRemaining


    def __str__(self):
        return self.grant_name

    class Meta:
            db_table = "Grants"

class GrantLine(models.Model):
    grantline_id = models.AutoField(primary_key=True, verbose_name="Line ID")
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, verbose_name="Grant")
    fund_year = models.SmallIntegerField(blank=False, verbose_name="Fund Year")
    line_name = models.CharField(max_length=255, verbose_name="Line Name")
    line_budgeted = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budgeted")
    #line_budget_remaining = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Remaining")
    #line_encumbered = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Encumbered")
    #line_budget_spent = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budget Spent")
    #line_total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Income")
    cofund = models.CharField(max_length=3, verbose_name="CoFund")
    gen_ledger = models.IntegerField(blank=False, verbose_name="General Ledger")
    county_code = models.CharField(max_length = 4, verbose_name="County Code")
    lineType = models.CharField(choices=[("Revenue","Revenue"), ("Expense", "Expense")], verbose_name="Line Type")

    @property
    def budgetSpent(self):
        expenses = Expense.objects.filter(grantLine__grantline_id=self.grantline_id)
        total = 0
        for expense in expenses:
            total += expense.amount
        
        return f"{total:.2f}"
    
    @property
    def budgetRemaining(self):
        remaining = float(self.line_budgeted) - float(self.budgetSpent)

        return f"{remaining:.2f}"
    
    @property
    def totalIncome(self):
        revenues = Revenue.objects.filter(grantLine__grantline_id = self.grantline_id)
        total = 0
        for revenue in revenues:
            total += revenue.amount
        
        return f"{total:.2f}"

    def clean(self):
        lines = GrantLine.objects.filter(grant = self.grant)
        total = 0
        revenueLines = 0
        for line in lines:
            if line.grantline_id != self.grantline_id:
                total += line.line_budgeted
                if line.lineType == "Revenue":
                    revenueLines += 1
        totalSum = total + self.line_budgeted

        if (revenueLines >= self.grant.maxRevenueLines) and (self.lineType == "Revenue"):
            raise ValidationError({"lineType": "Already have the max amount of revenue lines for the grant"})

        if self.grant.award_amount < totalSum:
            raise ValidationError({"line_budgeted":"Budgeted is more than is left in Grant Award"})
  
    def save(self, *args, **kwargs):
        #Check if this is the first time calling save on this object
        creating = self._state.adding


        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)

    def __str__(self):
        return self.line_name

    class Meta:
        db_table = "Grant Lines"

#Have a table made but dont use it right now
class GrantItem(models.Model):
    item_id = models.AutoField(primary_key=True, verbose_name="Item ID")
    fund_type = models.CharField(max_length=50, choices=FundSource.choices, verbose_name="Fund Type")
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    fund_year = models.IntegerField(verbose_name="Fund Year")
    item_name = models.CharField(max_length=255, verbose_name="Item Name")
    line_item = models.CharField(max_length=255, verbose_name="Line")
    category = models.CharField(max_length=50, verbose_name="Category")
    fee_based = models.BooleanField(verbose_name="Fee Based")
    month = models.IntegerField(verbose_name="Month")

    class Meta:
        db_table = "Grant Items"

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
    
    def __str__(self):
        return self.ba_id

    class Meta:
        db_table = "Budget Actions"
 
class Carryover(models.Model):
    co_id = models.AutoField(primary_key=True, verbose_name="Carryover ID")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name="Fund")
    fy = models.IntegerField(verbose_name="Fiscal Year") #fiscal year, max length 4
    co_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Carryover Amount")
    encumbered = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Encumbered")
    year_end_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Year-End Balance")
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, verbose_name="Department")
    beg_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Beginning Balance")
    fy_beg_date = models.DateField(verbose_name="Fiscal Year Beginning Date")
    fy_end_date = models.DateField(verbose_name="Fiscal Year End Date")
    
    def __str__(self):
        return self.co_id

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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    hrs_per_pay = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Hours Per Pay")
    vac_elig = models.BooleanField(default=True, verbose_name="Vacation Eligible") #not sure on default
    ins_type = models.CharField(max_length=10, choices=HealthInsurance.choices, verbose_name="Insurance Type")
    board_ins_share = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Board Insurance Share")
    life_rate = models.CharField(max_length=10, choices=LifeInsurance.choices, verbose_name="Life Insurance Rate")

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
            factor = Variable.objects.get(name="insuranceRate1").value
        elif rate == LifeInsurance.rate2:
            factor = Variable.objects.get(name="insuranceRate2").value
        
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
    
    def __str__(self):
        return self.employee

    class Meta:
            db_table = "Benefits"
 

class transactionType(models.TextChoices):
    revenue = "Revenue"
    expense = "Expense"
class paymentType(models.TextChoices):
    cash = "Cash"
    card = "Card"
    check = "Check"

class Revenue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    people = models.ForeignKey(People, on_delete=models.PROTECT, verbose_name="People")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Amount")
    payType = models.CharField(max_length=20, choices=paymentType.choices, verbose_name="Payment Type")
    confirmation = models.CharField(max_length=500, verbose_name="Confirmation")
    comment = models.CharField(max_length=500, verbose_name="Comment")
    ActivityList = models.ForeignKey(ActivityList, on_delete=models.PROTECT, verbose_name="Activity List")
    line = models.ForeignKey(Line, on_delete=models.PROTECT, verbose_name="Line")
    #odhafr = models.CharField(max_length=50, verbose_name="ODH AFR")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Employee")
    grantLine = models.ForeignKey(GrantLine, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Grant Line")


    def __str__(self):
        return (str(self.date) + " $" + str(self.amount))
    
    class Meta:
        db_table = "Revenue"

class Expense(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    people = models.ForeignKey(People, on_delete=models.PROTECT, verbose_name="People")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Amount")
    warrant = models.IntegerField(verbose_name="Warrant")
    comment = models.CharField(max_length=500, verbose_name="Comment")
    ActivityList = models.ForeignKey(ActivityList, on_delete=models.PROTECT, verbose_name="Activity List")
    line = models.ForeignKey(Line, on_delete=models.PROTECT, verbose_name="Line")
    #odhafr = models.CharField(max_length=50, verbose_name="ODH AFR")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Employee")
    grantLine = models.ForeignKey(GrantLine, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Grant Line")

    def clean(self):
        line = self.item.line
        self.line = line
        fund = line.fund
        if self.grantLine:
            if float(self.amount) > float(self.grantLine.budgetRemaining):
                raise ValidationError({"amount": "Amount is greater than remaining budget in Grant Line"})
        if float(self.amount) > float(self.line.budgetRemaining):
            raise ValidationError({"amount": "Amount is greater than remaining budget in Line"})
        
        if float(self.amount ) > float(fund.fund_cash_balance):
            raise ValidationError({"amount": "Amount is greater than remaining cash balance in Fund"})
    def save(self, *args, **kwargs):
        #Check if this is the first time calling save on this object
        creating = self._state.adding

        if creating:
            self.line = self.item.line


        self.full_clean()
        with transaction.atomic():
            fund = self.line.fund
            super().save(*args, **kwargs)
            fund.fund_cash_balance -= self.amount
            fund.save()


    def __str__(self):
        return (str(self.date) + " $" + str(self.amount))

    class Meta:
        db_table = "Expense"

class AccessControl(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        permissions = [("has_full_access", "Has full access to all views")]

"""
class Clockify(models.Model):
    ActivityList = models.ForeignKey(ActivityList, on_delete=models.PROTECT)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    startDate = models.CharField(max_length=255)
    endDate = models.CharField(max_length=255)
    billableRate = models.DecimalField(max_digits=10, decimal_places=2)
    billableAmount = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "Clockify"
"""

class Testing(models.Model):
    testing_name = models.CharField(max_length=200, blank=True)
    fund_year = models.IntegerField(blank=True, null = True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)

    @property
    def fundBalanceMinus3(self):
        return self.fund.fund_cash_balance - 3

    class Meta:
        db_table = "Testing"

