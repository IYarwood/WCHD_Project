from django import forms
from .models import Fund
from django.apps import apps

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["fund_id","fund_name", "fund_cash_balance", "dept_id", "sof", "mac_elig"]

class TableSelect(forms.Form):
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)