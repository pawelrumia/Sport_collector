from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_exercise, name='add_exercise'),
    path('get/', views.get_exercises, name='get_exercises'),
    path('update/', views.update_exercise_details, name='update_exercise'),
    path('form/', views.exercise_form, name='exercise_form'),
]
