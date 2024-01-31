from django.urls import path
from . import  views
from knox.views import LogoutView

app_name="core"
urlpatterns = [
    path('login', views.login_api, name='login_api'),
    path('register', views.register_api, name='register_api'),
    path('logout',LogoutView.as_view() , name='logout'),
    path('list-users',views.ListUser.as_view(), name='users_list'),
    path('login-page',views.login, name="login_page"),
    path("",views.user_list, name="list_users"),
    path('signup' , views.signup, name='signup'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         views.UserConfirmEmailView.as_view(), name='confirm_email'),
]
