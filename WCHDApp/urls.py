from django.urls import path
from . import views

urlpatterns = [
    path("", views.logIn, name="logIn"),
    path('index/', views.index, name='index'),
    path("newFund/", views.newFund, name="newFund"),
    path("tableView/<str:tableName>/", views.tableView, name="tableView"),
]