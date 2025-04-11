from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fund, Testing, Item
from .forms import FundForm, TableSelect, LineForm, InputSelect, ExportSelect,reconcileForm
from django.forms import modelform_factory
from django.apps import apps
from django.db.models import DecimalField
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import numpy as np
import json

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
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="testing.pdf"'

    return response

@permission_required('WCHDApp.has_full_access', raise_exception=True)
def reconcile(request):
    if request.method == "POST":
        form = reconcileForm(request.POST, request.FILES)
        if form.is_valid():
            firstFile = form.cleaned_data['firstFile'] 
            secondFile = form.cleaned_data['secondFile'] 
            
            df1 = pd.read_csv(firstFile)
            df2 = pd.read_csv(secondFile)

            columnList = list(df1.columns)
            for i in range(len(columnList)):
                columnList[i] = columnList[i].strip()
            # Merge the two lists and remove duplicates
            merged_df = pd.concat([df1, df2]).drop_duplicates()

            # Identify common entries (entries in both list1 and list2)
            common_entries = df1.merge(df2, on=columnList, how="inner")

            # Save merged data to an Excel file
            output_file = "output.xlsx"
            merged_df.to_excel(output_file, index=False)

            # Load the saved Excel file for formatting
            wb = load_workbook(output_file)
            ws = wb.active

            # Define highlight style
            highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

            # Convert common entries into a set for fast lookup
            rows = common_entries[columnList].apply(tuple, axis=1)
            common_set = set(rows)
            print(common_set)

            # Apply highlighting to rows that are NOT common (i.e., unique to either list1 or list2)
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1):
                rowData = []
                for column in row:
                    rowData.append(column.value)
                rowTuple = tuple(rowData)
                print(rowTuple)
                if rowTuple not in common_set:  # Highlight unique entries only
                    for cell in row:
                        cell.fill = highlight_fill
            
            outputStream = BytesIO()
            wb.save(outputStream)
            outputStream.seek(0)
            response = HttpResponse(outputStream.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="reconciliation.xlsx"'

            return response
    else:
        form = reconcileForm()
    return render(request, "WCHDApp/reconcile.html", {"form":form})

#This view is used to select what table we want to create a report from
@permission_required('WCHDApp.has_full_access', raise_exception=True)
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
@permission_required('WCHDApp.has_full_access', raise_exception=True)
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
@permission_required('WCHDApp.has_full_access', raise_exception=True)
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
        "Payroll": [("pay_rate", "Pay Rate")]
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
@permission_required('WCHDApp.has_full_access', raise_exception=True)
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

@permission_required('WCHDApp.has_full_access', raise_exception=True)
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

@permission_required('WCHDApp.has_full_access', raise_exception=True)
def imports(request):
    message = ""
    if request.method == 'POST':
        form = InputSelect(request.POST, request.FILES)
        if form.is_valid():
            tableName = form.cleaned_data['table']
            selectedFile = form.cleaned_data['file']
            file = pd.read_csv(selectedFile)
            columns = file.columns
            row = file.iloc[0]
            data = []
            model = apps.get_model('WCHDApp', tableName)
            fields = model._meta.get_fields()

            neededFields = []
            for field in fields:
                if not field.auto_created:
                    neededFields.append(field.name)
            
            if neededFields != list(columns):
                message = "Bad File. Please check your CSV format and try again."
                return render(request, "WCHDApp/imports.html", {"form": form, "message": message})
            lookUpFields = []
            fks = []
            for field in fields:
                #Logic for foreign keys
                if field.is_relation:
                    fks.append(field.name)
                    if field.auto_created:
                        continue
                    else:
                        #Grab related model. This is why foreign keys have to be named after the model 
                        parentModel = apps.get_model('WCHDApp', field.name)

                        #Get the related models primary key
                        fkName = parentModel._meta.pk.name
                        #fks.append(fkName)
                        #Primary keys verbose name
                        fkAlias = parentModel._meta.pk.verbose_name
                else:
                    lookUpFields.append(field)
            

            print(fks)
            for i in range(len(file)):
                dict = {}
                row = file.iloc[i]
                for column in columns:
                    dict[column] = row[column]
                data.append(dict)
                
            
            for line in data:
                for key in line:
                    if type(line[key]) == np.int64:
                        line[key] = int(line[key])
                    if key in fks:
                        parentModel = apps.get_model('WCHDApp', key)
                        print("Grab the object linked")
                        line[key] = parentModel.objects.get(pk=line[key])
                print(line)
                obj, _ = model.objects.update_or_create(
                    **line,
                    defaults = line
                )    
    else:
        form = InputSelect()
    
        
    return render(request, "WCHDApp/imports.html", {"form": form, "message": message})

@permission_required('WCHDApp.has_full_access', raise_exception=True)
def exports(request):
    message = ""
    if request.method == 'POST':
        form = ExportSelect(request.POST)
        if form.is_valid():
            tableName = form.cleaned_data['table']
            fileName = form.cleaned_data['fileName']
            model = apps.get_model('WCHDApp', tableName)
            data = model.objects.all().values()
            exportData = pd.DataFrame.from_records(data)

            #From what I read the 2 commented lines are how we can show it in a new tab before download
            #However, its raw text apparently browsers dont like not immediately downloading csv, could be useful for our reports though
            response = HttpResponse(content_type='text/csv')
            #response = HttpResponse(content_type='text/text')
            #response['Content-Disposition'] = f'inline; filename="{fileName}.csv"'
            response['Content-Disposition'] = f'attachment; filename="{fileName}.csv"'

            exportData.to_csv(path_or_buf=response, index=False)
            return response
    else:
        form = ExportSelect()
        
    return render(request, "WCHDApp/exports.html", {"form": form, "message": message})

def transactionsItem(request):
    itemModel = apps.get_model('WCHDApp', "Item")
    itemValues = itemModel.objects.all()
    if request.method == "POST":
        itemID = request.POST.get('itemSelect')
        return redirect(transactionsView,itemID)
    
    return render(request, "WCHDApp/transactionsItem.html", {"items":itemValues})

def transactionsView(request,itemID):
    transactionModel = apps.get_model('WCHDApp', "transaction")
    transactionValues = transactionModel.objects.filter(item_id=itemID)

    #Getting just field names from model
    fields = transactionModel._meta.get_fields()

    #Lists to sort fields for styling
    fieldNames = []
    decimalFields = []
    aliasNames = []

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

    TransactionForm = modelform_factory(transactionModel, exclude=(["fund", "line", "item"]))
    item = Item.objects.get(pk=itemID)
    fund = item.fund
    line = item.line

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Create the instance but don't save it yet
            transaction = form.save(commit=False)

            # Attach the fund and line from the item
            transaction.fund = fund
            transaction.line = line
            transaction.item = item

            # Now save it
            transaction.save()

    else:
        form = TransactionForm()

    return render(request, "WCHDApp/transactionsView.html", {"item": itemID, "transactions": transactionValues,"fields": fieldNames, "aliasNames": aliasNames, "data": transactionValues, "decimalFields": decimalFields, "form":form})

def testing(request):
    if (request.user.is_superuser):
        if request.method == 'POST':
            form = InputSelect(request.POST, request.FILES)
            if form.is_valid():
                tableName = form.cleaned_data['table']
                
        else:
            form = InputSelect()
        
            
        return render(request, "WCHDApp/testing.html", {"form": form})
    else:
        return redirect(noPrivileges)

def checkPrivileges(request):
    print("Checking privileges")
    if (request.user.is_staff):
        print("Staff")
        return redirect(noPrivileges)  
    else:
        return None 
    
def noPrivileges(request, exception):
    return render(request, "WCHDApp/noPrivileges.html")
