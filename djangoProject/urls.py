"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from djangoProject import views, video, elderly_info, volunteer_info, employee_info
from djangoProject.views import send_code

from .elderly_info import create_elderly_record

urlpatterns = [  # urls
    path('fornow',views.fornow),
    path('register', views.register),
    path('display', video.video),
    path('send_code', send_code),
    path('login', views.login),
    path('edit', views.edit_admin_info),
    path('detail', views.get_detail),
    path('events/total', views.get_event),
    path('elderly/analysis', elderly_info.send_data),
    path('elderly/create', elderly_info.create_elderly_record),
    path('elderly/profile', elderly_info.shot_elderly_profile),
    path('elderly/collect', elderly_info.collect_elderly_face),
    path('elderly/total', elderly_info.show_all_elderly),
    path('elderly/delete', elderly_info.delete_elderly),
    path('elderly/edit', elderly_info.edit_elderly),
    path('elderly/rate', elderly_info.detect_heart_rate),
    path('volunteer/create', volunteer_info.create_volunteer_info),
    path('volunteer/profile', volunteer_info.shot_volunteer_profile),
    path('volunteer/collect', volunteer_info.collect_volunteer_face),
    path('volunteer/total', volunteer_info.show_all_volunteer),
    path('volunteer/edit', volunteer_info.edit_volunteer),
    path('volunteer/delete', volunteer_info.delete_volunteer),
    path('employee/create', employee_info.create_employee_info),
    path('employee/profile', employee_info.shot_employee_profile),
    path('employee/collect', employee_info.collect_employee_face),
    path('employee/total', employee_info.show_all_employee),
    path('employee/edit', employee_info.edit_employee),
    path('employee/delete', employee_info.delete_employee),
    path('changePwd', views.change_pwd),
    path('changePwd_send_code', views.send_code_changePwd),
    path('changePwd_forget', views.forget_changePwd),
]

