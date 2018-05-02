from django.urls import path

# import views from current directory
from . import views

urlpatterns = [
    # codingbot.com/
    path('', views.LoginFormView.as_view(), name='login'),
    # codingbot.com/professor
    path('professor', views.professor, name='professor'),
	# codingbot.com/professorView
	path('professorView', views.classEditFormView.as_view(), name='professorView'),
	# codingbot.com/professorCreate
	path('professorCreate', views.classCreationFormView.as_view(), name='professorCreate'),
    # codingbot.com/register
    path('register', views.UserRegistrationFormView.as_view(), name='register'),
    # codingbot.com/school
    path('school', views.school, name='school'),
	# codingbot.com/schoolView
	path('schoolView', views.schoolView, name='schoolView'),
	# codingbot.com/schoolCreate
	path('schoolCreate', views.professorCreationFormView.as_view(), name='schoolCreate'),
    # codingbot.com/student
    path('student', views.studentMenuFormView.as_view(), name='student'),
    # codingbot.com/logout
    path('logout', views.logout_view, name='logout'),
    # codingbot.com/login_error
    path('login_error', views.login_error, name='login_error'),
]