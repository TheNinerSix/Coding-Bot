from django.urls import path

# import views from current directory
from . import views

urlpatterns = [
    # codingbot.com/
    path('', views.LoginFormView.as_view(), name='login'),
    # codingbot.com/professor
    path('professor', views.professor, name='professor'),
    # codingbot.com/register
    path('register', views.UserRegistrationFormView.as_view(), name='register'),
    # codingbot.com/school
    path('school', views.school, name='school'),
    # codingbot.com/student
    path('student', views.studentMenuFormView.as_view(), name='student'),
    # codingbot.com/logout
    path('logout', views.logout_view, name='logout'),
    # codingbot.com/login_error
    path('login_error', views.login_error, name='login_error'),
    # codingbot.com/add_class
    path('add_class', views.AddClassFormView.as_view(), name='add_class'),
    # codingbot.com/pack_select
    path('pack_select', views.PackSelectFormView.as_view(), name='pack_select'),
]