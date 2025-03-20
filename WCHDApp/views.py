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


    # Create a table with Fund names and details
    data = [
        fieldNames,
    ]
    for row in values:
        line = []
        for field in fields:
            line.append(row.field)
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


def index(request):
    return render(request, "WCHDApp/index.html")

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

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #If authentication is successful, returns related user object
        #notAdmin pass is Marietta123
        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "WCHDApp/logIn.html")

def viewTableSelect(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)
        button = request.POST.get('button')
        print("ACTION: " + str(button))
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            if button == "seeTable":
                return redirect('tableView', tableName)
            elif button == "create":
                return redirect('createEntry', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/viewTableSelect.html", {'form': form})

def tableView(request, tableName):
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
    return render(request, "WCHDApp/tableView.html", {"fields": fieldNames, "aliasNames": aliasNames, "data": values, "tableName": tableName, "decimalFields": decimalFields})

def createSelect(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            return redirect('createEntry', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/createSelect.html", {'form': form})

def createEntry(request, tableName):
    model = apps.get_model('WCHDApp', tableName)
    if request.method == 'POST':
        form = modelform_factory(model, fields="__all__")(request.POST)
        #Can use something like this 
        #date = request.POST.get('fund_year')
        #print(date)
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

