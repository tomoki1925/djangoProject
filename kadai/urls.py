from django.urls import path
from . import views

app_name = 'kadai'

urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout, name="logout"),
    path('top', views.loginTop, name="top"),
    path('employee', views.employee, name="employee"),
    path('employee_check', views.employee_check, name="employee_check"),
    path('employee_back', views.employee_back, name="employee_back"),
    path('hospitalList', views.hospital_list, name="hospital_list"),
    path('telcheck', views.telcheck, name="telcheck"),
    path('comit', views.telcomit, name="comit"),
    path('CSearch', views.CSearch, name="CSearch"),
    path('CSearch2', views.CSearch2, name="CSearch2"),
    path('emppass', views.emppass, name="emppass"),
    path('manager_pass', views.manager_pass, name="manager_pass"),
    path('uke_pass', views.uke_pass, name="uke_pass"),
    path('patiReg', views.patiReg, name="patiReg"),
    path('patient_reg', views.patient_reg, name="patient_reg"),
    path('patich', views.patich, name="patich"),
    path('patient/<str:patid>', views.patich2, name="patich2"),
    path('patient_ch', views.patient_ch, name="patient_ch"),
    path('patient_dec', views.patient_dec, name="patient_dec"),
    path('patient_top', views.patient_top, name="patient_top"),
    path('patserch', views.patserch, name="patserch"),
    path('zpats', views.zpats, name="zpatis"),
    path('patiidse', views.patiidse, name="patiidse"),
    path('zenken', views.zenken, name="zenken"),
    path('isi_top', views.isi_top, name="isi_top"),
    path('drug/<str:pid>', views.drug, name="drug"),
    path('drug_check', views.drug_check, name="drug_check"),
    path('del_drug/<str:delid>', views.del_medicine, name="del_medicine"),
    path('drug_top', views.drug_top, name="drug_top"),
    path('treatment', views.treatment, name="treatment"),
    path('history', views.history, name="history"),
    path('treatment_history', views.treatment_history, name="treatment_history"),
]
