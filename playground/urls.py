from django.urls import path
from . import views

#URLConf
urlpatterns = {
    path('board/', views.load_board),
}