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
from django.urls import path
from djangoProject import views, video, elderly_info
from djangoProject.views import send_code
from .testvideo import url

urlpatterns = [  # urls
    path('register', views.register),
    path('display', video.video),
    path('send_code', send_code),
    path('login', views.login),
    path('edit', views.edit_admin_info),
    path('elderly/create', elderly_info.create_elderly_record),
    path('elderly/profile', elderly_info.shot_elderly_profile),
    path('elderly/total', elderly_info.show_all_elderly),
    path('changePwd', views.change_pwd),
    path('changePwd_send_code', views.send_code_changePwd),
    path('changePwd_forget', views.forget_changePwd),
]

