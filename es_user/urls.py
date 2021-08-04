from es_user import views
from django.urls import path


urlpatterns = [
    path('', views.UserView.as_view(), name='user-home'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
]
