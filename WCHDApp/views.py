from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fund
from .forms import FundForm, TableSelect
from django.apps import apps

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TableSelect(request.POST)
        if form.is_valid():
            tableName = form.cleaned_data['table'] 
            return redirect('tableView', tableName=tableName)
    else:
        form = TableSelect()
    return render(request, "WCHDApp/index.html", {'form': form})

def newFund(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        form.save()
        return redirect('index')
    else:
        form = FundForm()
    
    return render(request, "WCHDApp/newFund.html", {'form': form})

def logIn(request):
    if request.method == 'POST':
        return redirect('index')
    return render(request, "WCHDApp/logIn.html")

def tableView(request, tableName):
    model = apps.get_model('WCHDApp', tableName)
    objects = model.objects.all().values()
    fields = [field.name for field in model._meta.get_fields()]
    context = {
            "fields": fields,   # List of field names (headers)
            "data": objects,    # QuerySet as dictionaries
            "tableName": tableName
        }

    return render(request, "WCHDApp/tableView.html", context)