"""
URL configuration for ninja_brain project.

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
from django.urls import path
from ninja import NinjaAPI
from .api import router as home_router
from nlp.api import router as nlp_router

api = NinjaAPI()

api.add_router("/", home_router)
api.add_router("/nlp/", nlp_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", api.urls),
    path("api/", api.urls),
]
