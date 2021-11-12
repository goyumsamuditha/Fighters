from django.conf.urls import url
from . import views

app_name = 'HR'
urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^employee_profile/', views.employee_profile, name='employee_profile'),
    url(r'^home/', views.home, name='home'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^employee_leaves/', views.employee_leaves, name='employee_leaves'),
    url(r'^requested_leaves/', views.requested_leaves, name='requested_leaves'),
    url(r'^about/', views.about, name='about'),
    url(r'^display_leaves/', views.display_leaves, name='display_leaves'),
]