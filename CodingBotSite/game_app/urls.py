from django.urls import path

# import views from current directory
from . import views

urlpatterns = [
    # codingbot.com/game
    path('', views.studentGameFormView.as_view(), name='game'),
]