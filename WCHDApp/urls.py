from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.logIn, name="logIn"),
    path('index/', views.index, name='index'),
    path("newFund/", views.newFund, name="newFund"),
    path("newLine/", views.newLine, name="newLine"),
    path("tableViewSelect/", views.viewTableSelect, name="viewTableSelect"),
    path("tableView/<str:tableName>/", views.tableView, name="tableView"),
    path("createSelect/", views.createSelect, name="createSelect"),
    path("createEntry/<str:tableName>/", views.createEntry, name="createEntry"),
    path("testing/", views.testing, name="testing"),
    path('generate_pdf/<str:tableName>/', views.generate_pdf, name='generate_pdf'),
    path('reports/', views.reports, name='reports'),
    path('imports/', views.imports, name='imports'),
    path('exports/', views.exports, name='exports'),
    path('countyPayrollExport/', views.countyPayrollExport, name='countyPayrollExport'),
    path('transactionsItem/', views.transactionsItem, name='transactionsItem'),
    path('transactionsView/', views.transactionsView, name='transactionsView'),
    path('noPrivileges/', views.noPrivileges, name='noPrivileges'),
    path('reconcile/', views.reconcile, name='reconcile'),
    path('dailyReport/', views.dailyReport, name='dailyReport'),
    path('clockifyImport/', views.clockifyImport, name='clockifyImport'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('calculateActivitySelect/', views.calculateActivitySelect, name='calculateActivitySelect'),
    path('getActivities/', views.getActivities, name='getActivities'),
    path('clockifyImportPayroll/', views.clockifyImportPayroll, name='clockifyImportPayroll'),
    path('payrollView/', views.payrollView, name='payrollView'),
    path('fundSummary/', views.fundSummary, name='fundSummary'),
    path('activitySummary/', views.activitySummary, name='activitySummary'),
    path('employeeSummary/', views.employeeSummary, name='employeeSummary'),
    path('transactionCustomView/', views.transactionCustomView, name='transactionCustomView'),
    path('transactionsExpenses/', views.transactionsExpenses, name='transactionsExpenses'),
    path('transactionsExpenseTableUpdate/', views.transactionsExpenseTableUpdate, name='transactionsExpenseTableUpdate'),
    path('addPeopleForm/', views.addPeopleForm, name='addPeopleForm'),
]

    
    

