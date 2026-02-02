from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="start"),
    path('regi1/', views.regi1_input, name="regi1_input"),
    path('regi1/result/', views.regi1_result, name="regi1_result"),
    path('regi2/', views.regi2_input, name="regi2_input"),
    path('regi2/result/', views.regi2_result, name="regi2_result"),
    path('cash_total/', views.cash_total, name="cash_total"),
    path('sales/', views.sales_input, name="sales_input"),
    path('sales/result/', views.sales_result, name="sales_result"),
    path('miss/', views.miss_input, name="miss_input"),
    path('miss/result/', views.miss_result, name="miss_result"),
    path('gift/', views.gift_input, name="gift_input"),
    path('shareholder/', views.shareholder_input, name="shareholder_input"),
    path('credit/', views.credit_input, name="credit_input"),
    path('credit/result/', views.credit_result, name="credit_result"),
    path('md/', views.md_input, name="md_input"),
    path('change/', views.change_input, name="change_input"),
    path('summary/', views.summary_view, name="summary"),
    path('final/', views.final_result, name="final_result"),
]
