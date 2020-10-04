"""DP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from . import views
from accounts.views import signup_view, activation_sent_view, activate, post_detail_view, signup
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from accounts import forms
from django.contrib.auth.views import LoginView
from . import views, settings

from django_otp.admin import OTPAdminSite
class OTPAdmin(OTPAdminSite):
    pass

from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)
admin.site.site_header = "URBAN DELIVERY"
admin.site.site_title = "URBAN DELIVERY ADMIN PORTAL"
admin.site.index_title = "WELCOME TO URBAN DELIVERY ADMIN PORTAL"


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/', views.user_login, name='admin'),
    #path('posts/', views.post_detail_view.as_view()),
    url(r'',include('accounts.urls')),
    #url(r'^$',views.HomePage.as_view(),name='home'),
    url(r'^$',views.delivery_person_view, name='home'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^signup/$', signup, name="signup"),
    url(r'^thanks/$', views.HomePage.as_view(), name='thanks'),
    url(r'^admin_site/$',views.AdminPage.as_view(), name='adminpage'),
    url(r'validate/$', views.Validateuser, name='validate_login'),
    url(r'^$', views.ValidateOTP, name='validate_otp'),
    url(r'^saved/', views.HomePage.as_view(), name ='saved'),
    url(r'^employee/$',views.Employee, name='delivery'),
    url(r'^download/$',views.download, name='download'),
    path('accounts/login/', LoginView.as_view(authentication_form=forms.OTPAuthenticationForm), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
