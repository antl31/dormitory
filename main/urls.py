"""diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, re_path, path
from rest_framework import routers

from .views import RoomViewSet, UserViewSet, blank_a4, blank_a5, pdf_template_statistics


router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'v1/', include('rest_auth.urls')),  # v1/login/# POST
    path(r'blanks/admin', pdf_template_statistics),
    path(r'blanks/full/<id>/', blank_a4),
    path(r'blanks/small/<id>/', blank_a5)

]
