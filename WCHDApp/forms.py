from django import forms
from .models import Fund,Line
from django.apps import apps

#New Fund Form/ sets up inputs for the given fields of the model
class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["fund_id","fund_name", "fund_cash_balance", "dept", "sof", "mac_elig"]

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ["fund","fund_year", "line_name", "line_budgeted", "line_encumbered", "line_budget_spent", 
                  "line_total_income", "dept", "cofund", "gen_ledger", "county_code"]



#Index Form/ Normal form that gives a drop down of tables included in models.py. 
class TableSelect(forms.Form):
    #Pulling models
    models = apps.get_app_config('WCHDApp').get_models()
    modelsDict= {}
    for model in models:
        modelsDict[model.__name__] = model.__name__
    table = forms.ChoiceField(choices=modelsDict, label="Select Table", required=True)