from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fund
from .forms import FundForm, TableSelect, LineForm
from django.forms import modelform_factory
from django.apps import apps
from django.db.models import DecimalField
from django.contrib.auth import authenticate, login
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from io import BytesIO

def generate_pdf(request, tableName):
    buffer = BytesIO()

    # Create a PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=16,
        spaceAfter=11,
        fontName="Helvetica-Bold"
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=6,
        fontName="Helvetica-Oblique"
    )


    #logo = Image("logo.png", width=80, height=80)
    #logo.hAlign = 'LEFT'
    #elements.append(logo)

    elements.append(Spacer(1, 12))

    # Report Title
    elements.append(Paragraph("Washington County Health Department", title_style))
    elements.append(Paragraph(
        "List of Active Grants. Active means they have been awarded and the final expenditure report has not yet been approved.",
        subtitle_style
    ))

    elements.append(Spacer(1, 12))

    #Same logic as tableView, needs updated to current 
    model = apps.get_model('WCHDApp', tableName)
    values = model.objects.all().values()
    fields = model._meta.get_fields()
    fieldNames = []
    decimalFields = []
    aliasNames = []
    for field in fields:
        if field.is_relation:
            if field.auto_created:
                continue
            else:
                parentModel = apps.get_model('WCHDApp', field.name)
                fkName = parentModel._meta.pk.name
                fkAlias = parentModel._meta.pk.verbose_name
                aliasNames.append(fkAlias)
                fieldNames.append(fkName)

        else:
            if isinstance(field, DecimalField):
                decimalFields.append(field.name)
            aliasNames.append(field.verbose_name)  
            fieldNames.append(field.name)

    data = [
        aliasNames,
    ]
    
    for row in values:
        print(row)
        line = []
        for field in fieldNames:
            line.append(row[field])
        data.append(line)


    # Table Styling
    table = Table(data, colWidths=[80, 70, 70, 70, 70, 50, 100, 50, 90, 40])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    # Totals (below table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Total Active Grants:</b> $571,880.00", styles["Normal"]))
    elements.append(Paragraph("<b>Total Amount for Project:</b> $19,144.00", styles["Normal"]))

    #Build PDF
    doc.build(elements)

    # Get the PDF value from buffer
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="active_grants.pdf"'

    return response

#This view is used to select what table we want to create a report from
def reports(request):
    if request.method == "POST":
        #TableSelect is a form I defined in forms.py
        form = TableSelect(request.POST)

        #Take the data from the form and pass it to our pdf generator function
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            return redirect('generate_pdf', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/reports.html", {'form': form})

#Hub, does nothing yet
def index(request):
    return render(request, "WCHDApp/index.html")

#newFund and newLine are depricated, used in our old way of doing things
#Will eventually clean this system out
def newFund(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        form.save()
        return redirect('index')
    else:
        form = FundForm()
    
    return render(request, "WCHDApp/newFund.html", {'form': form})

def newLine(request):
    if request.method == 'POST':
        form = LineForm(request.POST)
        form.save()
        return redirect('index')
    else:
        form = LineForm()
    
    return render(request, "WCHDApp/newLine.html", {'form': form})


#Login page logic
def logIn(request):
    #Getting username and password from the form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #If authentication is successful, returns related user object
        #notAdmin pass is Marietta123
        #Django implemented function to check databse for user and rights etc
        user = authenticate(request, username = username, password=password)

        #If authenticated, login (Django function) and redirect to hub
        #If not give error 
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "WCHDApp/logIn.html")

#Logic to get what tables we want to see/create from. Same thing as reports
def viewTableSelect(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)

        #Logic to figure out which button sent the request so that we can correctly redirect
        #Each button has a different value aligning to their names, this is set in the html file "viewTableSelect"
        button = request.POST.get('button')
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            if button == "seeTable":
                return redirect('tableView', tableName)
            elif button == "create":
                return redirect('createEntry', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/viewTableSelect.html", {'form': form})

#This function decides what data we use in our tables in tableView.html
def tableView(request, tableName):

    #Grabbing the model selected in viewTableSelect
    model = apps.get_model('WCHDApp', tableName)

    #Getting data from that model
    values = model.objects.all()

    #Getting just field names from model
    fields = model._meta.get_fields()

    #Lists to sort fields for styling
    fieldNames = []
    decimalFields = []
    aliasNames = []

    #Any property that we define in models need to go here so our logic can include them in the table
    calculatedProperties = {
        #"Fund": [("fundBalanceMinus3", "Fund Balance Minus 3")],
        "Testing": [("fundBalanceMinus3", "Fund Balance Minus 3")],
        "Benefits": [("pers", "Public Employee Retirement System"), ("medicare", "Medicare"),("wc", "Workers Comp"), ("plar", "Paid Leave Accumulation Rate"), ("vacation", "Vacation"), ("sick", "Sick Leave"), ("holiday", "Holiday Leave"), ("total_hrly", "Total Hourly Cost"), ("percent_leave", "Percent Leave"), ("monthly_hours", "Monthly Hours"), ("board_share_hrly", "Board Share Hourly"), ("life_hourly", "Life Hourly"), ("salary", "Salary"), ("fringes", "Fringes"), ("total_comp", "Total Compensation")],
    }

    #This is used to decide which fields we want to show in the accumulator based on each model
    summedFields = {
        "Fund": "fund_cash_balance"
    }
    

    for field in fields:

        #Logic for foreign keys
        if field.is_relation:
            if field.auto_created:
                continue
            else:
                #Grab related model. This is why foreign keys have to be named after the model 
                parentModel = apps.get_model('WCHDApp', field.name)

                #Get the related models primary key
                fkName = parentModel._meta.pk.name

                #Primary keys verbose name
                fkAlias = parentModel._meta.pk.verbose_name

                aliasNames.append(fkAlias)
                fieldNames.append(fkName)
        else:
            #Decimal field logic so we can style them in html
            if isinstance(field, DecimalField):
                decimalFields.append(field.name)
            aliasNames.append(field.verbose_name)  
            fieldNames.append(field.name)
    
    #Making sure properties are added like normal fields to the tables
    if tableName in calculatedProperties:
        for property in calculatedProperties[tableName]:
            aliasNames.append(property[1])
            fieldNames.append(property[0])
            decimalFields.append(property[0])

    #Getting values based on if we defined them in summedFields in order to make accumulator
    if tableName in summedFields:
        field = summedFields[tableName]
        accumulator = 0
        for value in values:
            accumulator += getattr(value, field)
        context = {"fields": fieldNames, "aliasNames": aliasNames, "data": values, "tableName": tableName, "decimalFields": decimalFields, "accumulator": accumulator}
    else:
        context = {"fields": fieldNames, "aliasNames": aliasNames, "data": values, "tableName": tableName, "decimalFields": decimalFields}

    return render(request, "WCHDApp/tableView.html", context)

#Also depricated, will clean soon
def createSelect(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            return redirect('createEntry', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/createSelect.html", {'form': form})

#New system to dynamically create forms based of model
def createEntry(request, tableName):
    #Grabbing selected model in viewTableSelect
    model = apps.get_model('WCHDApp', tableName)

    if request.method == 'POST':
        #Django function that makes a form based off a provided model
        form = modelform_factory(model, fields="__all__")(request.POST)

        #Data validation then save to table linked to the model
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = modelform_factory(model, fields="__all__")
    return render(request, "WCHDApp/createEntry.html", {"form": form, "tableName": tableName})

def testing(request, tableName):
    model = apps.get_model('WCHDApp', tableName)
    if request.method == 'POST':
        form = modelform_factory(model, fields="__all__")(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = modelform_factory(model, fields="__all__")
    return render(request, "WCHDApp/testing.html", {"form": form})

