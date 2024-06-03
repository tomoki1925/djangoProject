from django.urls import path
from . import views

app_name = 'kadai'

urlpatterns = [
    path('',views.index,name="index"),
    path('top',views.loginTop,name="top"),
    path('employee',views.employee,name="employee"),
    path('employee_check',views.employee_check,name="employee_check"),
    path('employee_back',views.employee_back,name="employee_back"),
    path('hospitalList',views.hospital_list,name="hospital_list"),
    path('<str:id>',views.telchange,name="telchange"),
    path('<str:id>/<str:lastcheak>',views.telcheck,name="telcheck"),

]