from django.urls import path
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
    path("testing/<str:tableName>/", views.testing, name="testing"),
    path('generate_pdf/<str:tableName>/', views.generate_pdf, name='generate_pdf'),
    path('reports/', views.reports, name='reports'),
]