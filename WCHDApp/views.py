from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fund
from .forms import FundForm, TableSelect, LineForm
from django.forms import modelform_factory
from django.apps import apps

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
        return redirect('index')
    return render(request, "WCHDApp/logIn.html")

def viewTableSelect(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            return redirect('tableView', tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/viewTableSelect.html", {'form': form})

def tableView(request, tableName):
    model = apps.get_model('WCHDApp', tableName)
    values = model.objects.all().values()
    fields = model._meta.get_fields()
    fieldNames = []
    for field in fields:
        if field.is_relation:
            if field.auto_created:
                continue
            else:
                parentModel = apps.get_model('WCHDApp', field.name)
                fkName = parentModel._meta.pk.name
                fieldNames.append(fkName)
        else:
            fieldNames.append(field.name)

    return render(request, "WCHDApp/tableView.html", {"fields": fieldNames, "data": values, "tableName": tableName})

def testing(request, tableName):
    model = apps.get_model('WCHDApp', tableName)
    if request.method == 'POST':
        form = modelform_factory(model, fields="__all__")(request.POST)
        form.save()
        return redirect('index')
    else:
        form = modelform_factory(model, fields="__all__")
    return render(request, "WCHDApp/testing.html", {"form": form})

