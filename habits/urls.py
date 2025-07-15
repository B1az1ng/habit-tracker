from django.urls import path
from . import views

urlpatterns = [
    path('',            views.habit_list,    name='habit_list'),
    path('complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),
    path('delete/<int:habit_id>/',   views.delete_habit,   name='delete_habit'),
    path('register/',    views.register,      name='register'),
    path('', views.home),

]
