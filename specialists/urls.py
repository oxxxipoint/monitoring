from django.urls import path

from . import views

app_name = 'specialists'
urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table, name='table'),
    path('new/', views.spec_new, name='spec_new'),
    path('criteria/', views.show_criteria, name='show_criteria'),
    path('criteria/new/', views.new_criteria, name='new_criteria'),
    path('<int:spec_id>/', views.estimate, name='estimate'),
    path('<int:spec_id>/edit/', views.spec_edit, name='spec_edit'),
    path('<int:spec_id>/estim_edit/', views.estim_edit, name='estim_edit'),
    path('<int:spec_id>/delete/', views.spec_delete, name='spec_delete'),
]
