from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('login/', views.login, name="login"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'), 

]