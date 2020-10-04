from django.conf.urls import url
from accounts import views
from .views import signup_view, activation_sent_view, activate
from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
   url(r'^about/$',views.AboutView.as_view(),name='about'),
   url(r'^contact/$',views.DetailView.as_view(),name='contact'),
   url(r'login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   url(r'EmployeeLogin/$', auth_views.LoginView.as_view(template_name='blog/employee.html'), name='delivery'),
   url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
   re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
   re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
   path('post/new/', views.post_new, name='post_new'),
   url(r'^posts/', views.post_detail_view, name='post_list'),
   url(r'^profile/',views.SaveProfile, name='saveprofile'),
   url(r'^post/(?P<pk>\d+)$',views.PostDetailView,name='post_detail'),
   #path('', views.post_list, name='post_list'),
   #path('post/<int:pk>/', views.post_detail, name='post_detail'),
   url(r'post/new/amount',views.calculate_amount_view, name='calculate_amount'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
