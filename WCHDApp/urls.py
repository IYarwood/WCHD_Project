from django.urls import path
from . import views

urlpatterns = [
    path("", views.logIn, name="logIn"),
    path('index/', views.index, name='index'),
    path("newFund/", views.newFund, name="newFund"),
    path("newLine/", views.newLine, name="newLine"),
    path("tableViewSelect/", views.viewTableSelect, name="viewTableSelect"),
    path("tableView/<str:tableName>/", views.tableView, name="tableView"),
]