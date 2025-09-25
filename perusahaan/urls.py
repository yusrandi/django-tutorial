"""
URL configuration for perusahaan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from api.views import my_view
from user.views import UserView
from product.views import ProductView
from employee.views import EmployeeView
from rest_framework.routers import DefaultRouter

from user.views import RegisterView, LoginView

router = DefaultRouter()
router.register(r"users", UserView, basename="user")
router.register(r"products", ProductView, basename="product")
router.register(r"employees", EmployeeView, basename="employee")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", my_view),
    path("api/", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
