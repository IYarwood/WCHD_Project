from django import forms
from .models import Fund,Line, GrantExpense
from django.apps import apps

#New Fund Form/ sets up inputs for the given fields of the model
class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["fund_id","fund_name", "fund_cash_balance", "dept", "sof", "mac_elig"]

"""
class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ["fund","fund_year", "line_name", "line_budgeted", "line_encumbered", "line_budget_spent", 
                  "line_total_income", "dept", "cofund", "gen_ledger", "county_code"]
"""



#Index Form/ Normal form that gives a drop down of tables included in models.py. 
class TableSelect(forms.Form):
    #Pulling models
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True,  widget=forms.Select(attrs={'class': 'searchable-select'}))

class InputSelect(forms.Form):
    #Pulling models
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)
    file = forms.FileField(
        label="Upload CSV File",
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )

class FileInput(forms.Form):
    file = forms.FileField(
        label="Upload CSV File",
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )

class ExportSelect(forms.Form):
    #Pulling models
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)
    fileName = forms.CharField(max_length=20, label="File Name (do not include .csv)", required=True)

    

    
    """
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)
    """
    
class reconcileForm(forms.Form):
    firstFile = forms.FileField(
        label="Upload First CSV File",
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )
    secondFile = forms.FileField(
        label="Upload Second CSV File",
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )
   

class activitySelect(forms.Form):
    #Pulling models
    activityModel = apps.get_model('WCHDApp', 'ActivityList')
    activities = activityModel.objects.all()
    activityChoices = []
    for activity in activities:
        activityChoices.append((activity.ActivityList_id, activity.program))
    
    activityName = forms.ChoiceField(choices=activityChoices, label="Select Activity", required=True)
    
    
class GrantExpenseForm(forms.ModelForm):
    fund = forms.ModelChoiceField(queryset=Fund.objects.none())

    class Meta:
        model = GrantExpense
        exclude = ["fund", "grantline"]
    def __init__(self, *args, **kwargs):
        grant = kwargs.pop('grant', None)
        super().__init__(*args, **kwargs)

        self.fields['fund'].queryset = grant.fund.all()

    