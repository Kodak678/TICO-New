"""TICO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from playground import views as playground
from users import views as users


urlpatterns = [
    path('admin/', admin.site.urls),
    path('templates/board.html', playground.load_board),
    path('templates/login.html', users.login),
    path('templates/forgotten.html', users.forgotten),
    path('templates/leaderboard.html', users.leaderboard),
    path('templates/profile.html', users.profile),
    path('templates/updateDetails', users.updateDetails),
    path('templates/forgottenLogin', users.forgottenLogin),
    path('templates/register.html', users.register),
    path('templates/mainpage.html',playground.home),
    path('templates/authenticate',users.authenticate),
    path('boardStates', playground.boardStates),
    path('validMove', playground.validMove),
    path('AiMove', playground.AiMove),
    path('resetBoard', playground.resetBoard),
    path('getWinner', playground.getWinner),
    path('trainModel', playground.train_model),
    path('templates/addUser',users.addUser),
    path('',playground.home)
]
