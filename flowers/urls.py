from django.urls import path
from . import views

app_name = 'flowers'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.flower_add, name='flower_add'),
    path('flower/<int:pk>/', views.flower_detail, name='flower_detail'),
    path('delete/<int:pk>/', views.flower_delete, name='flower_delete'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]