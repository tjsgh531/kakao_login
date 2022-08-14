from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/', views.kakaoLogin, name="kakaoLogin"),
    path('callback/', views.kakaoCallback, name="kakaoCallback"),
]
