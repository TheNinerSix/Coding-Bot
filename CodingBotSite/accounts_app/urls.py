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
    # codingbot.com/game_print_statements
    path('game_print_statements', views.GamePrintStatementsFormView.as_view(), name='game_print_statements'),
    # codingbot.com/game_if_statements
    path('game_if_statements', views.GameIfStatementsFormView.as_view(), name='game_if_statements'),
    # codingbot.com/game_math_functions
    path('game_math_functions', views.GameMathFunctionsFormView.as_view(), name='game_math_functions'),
]

