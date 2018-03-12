from django.urls import path
from . import views

urlpatterns = [
    path('<str:hash>', views.blockInfo, name='blockInfo'),
    path('', views.latestBlockInfo, name='latestBlockInfo'),
]

