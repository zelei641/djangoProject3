"""djangoProject3 URL Configuration

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
from photoManage import views

urlpatterns = [
    path('photoupload/', views.photoupload),
    path('acm/admin/getUserUploaPhotoList/', views.getUserUploaPhotoList),
    path('acm/admin/admin/getUserUploadPhoto/', views.getUserUploadPhoto),
    path('acm/admin/admin/acmAdminProcessOkUpload/', views.acmAdminProcessOkUpload),
    path('user/userGetMyselfUploadPhotoList/', views.userGetMyselfUploadPhotoList),
    path('user/userGetRealPhoto/', views.userGetRealPhoto),
    path('acm/admin/getUserUploaPhotoListOk/', views.getUserUploaPhotoListOk),
]
