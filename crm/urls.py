from django.urls import path,re_path
from crm import views
urlpatterns = [
    # path('customer/', views.customer, name="customer"),
    path('page/', views.page),
    path('page2/', views.page2),
    # path('customer_add/', views.customer_add, name="customer_add"),
    path('customer_add/', views.customer_change, name="customer_add"),
    # re_path('^customer_edit/(\d+)/', views.customer_edit, name="customer_edit"),
    re_path('^customer_edit/(\d+)/', views.customer_change, name="customer_edit"),
    # path('my_customer/', views.customer, name="my_customer"),
    path('customer/', views.Customer.as_view(), name="customer"),
    path('my_customer/', views.Customer.as_view(), name="my_customer"),

    # 跟进记录相关
    re_path('consult/(?P<customer_id>\d+)', views.Consult.as_view(), name="consult"),
    path('consult_add', views.consult_add, name="consult_add"),
    re_path('consult_edit/(?P<edit_id>\d+)', views.consult_edit, name="consult_edit"),

    # 报名记录相关
    re_path('^enrollment/(?P<customer_id>\d+)', views.Enroll.as_view(), name="enrollment"),
    re_path('^enrollment_add/(?P<customer_id>\d+)', views.enrollment_add, name="enrollment_add"),
]