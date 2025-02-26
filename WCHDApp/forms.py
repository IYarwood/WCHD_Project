from django import forms
from .models import Fund
from django.apps import apps

#New Fund Form/ sets up inputs for the given fields of the model
class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["fund_id","fund_name", "fund_cash_balance", "dept_id", "sof", "mac_elig"]

#Index Form/ Normal form that gives a drop down of tables included in models.py. 
class TableSelect(forms.Form):
    #Pulling models
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)