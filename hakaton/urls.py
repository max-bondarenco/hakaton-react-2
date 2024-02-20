"""
URL configuration for hakaton project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from auction.views import index
from hakaton.views import sign_up, account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path(
        'auction/',
        include("auction.urls", namespace="auction"),
        name="auction"
    ),
    path('account/', account, name="account"),
    path('accounts/', include('django.contrib.auth.urls'), name="accounts"),
    path('sign-up/', sign_up, name="sign_up"),
    path('sign-up/verify/', sign_up, name="sign_up_verify"),
    path('sign-up/verify/success', account, name="sign_up_verify"),
    path('front/', include('frontend.urls', namespace='frontend'), name="frontend")
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

app_name = "auction_service"
