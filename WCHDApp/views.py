from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fund
from .forms import FundForm, TableSelect, LineForm
from django.forms import modelform_factory
from django.apps import apps
from django.db.models import DecimalField
from django.contrib.auth import authenticate, login
from django.contrib import messages

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

