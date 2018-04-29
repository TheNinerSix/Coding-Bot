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
    path('student', views.student, name='student'),    
]