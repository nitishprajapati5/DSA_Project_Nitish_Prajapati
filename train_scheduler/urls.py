from django.urls import path
from . import views


urlpatterns = [
    path('', views.train_board, name='train_board'),
    path('station/<str:station_code>/', views.train_board, name='station_board'),
    path('update-train/<str:train_id>/', views.update_train_status, name='update_train_status'),
]