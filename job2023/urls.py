"""job2023 URL Configuration

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
from django.urls import path, re_path
from django.views import static
import os
from api.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('personal/', personal),
    path('find_job/', find_job),
    path('job_detail/', job_detail),
    path('join_job2/', join_job2),
    path('join_status_list/', join_status_list),
    path('e_info/', e_info),
    path('job_delete/', job_delete),
    path('job_watting_profile/', job_watting_profile),
    path('check_pass/', check_pass),
    path('post_job/', post_job),
    path('admin_show_account_stu/', admin_show_account_stu),
    path('admin_show_account_e/', admin_show_account_e),
    path('work_list/', work_list),
    path('find_jobs/', find_jobs),
    path('change_password/', change_password),
    path('add_comment/<int:post_id>/', add_comment,name='add_comment'),
    path('add_post/', add_post),
    path('post_list/', post_list,name='post_list'),
    path('post_detail/<int:post_id>/', post_detail,name='post_detail'),
    path('test/', test, name='test'),
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': os.path.join(BASE_DIR, 'static')}),
]
