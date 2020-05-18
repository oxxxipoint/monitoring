from django.urls import path

from . import views

app_name = 'specialists'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.spec_new, name='spec_new'),
    path('criteria/', views.show_criteria, name='show_criteria'),
    path('criteria/set_default/', views.set_default, name='set_default'),
    path('criteria/new/', views.new_criteria, name='new_criteria'),
    path('<str:criteria_name>/delete/', views.delete_criteria, name='delete_criteria'),
    path('<int:spec_id>/', views.show_estimates, name='estimate'),
    path('<int:spec_id>/<str:estim_name>', views.estim_delete, name='estim_delete'),
    path('<int:spec_id>/edit/', views.spec_edit, name='spec_edit'),
    path('<int:spec_id>/estim_edit/', views.estim_edit, name='estim_edit'),
    path('<int:spec_id>/set_random/', views.set_random, name='set_random'),
    path('<int:spec_id>/delete/', views.spec_delete, name='spec_delete'),
]
