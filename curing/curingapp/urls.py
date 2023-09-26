from django.urls import path
from . import views
from . import exeriment

urlpatterns = [
    path('', views.login_user),
    path('home/',views.home,name='home'), 
    path('loginuser/', views.login_user, name='loginuser'),
    path('logoutuser/',views.logout_user,name='logoutuser'),
    path('registeruser/',views.register_user,name='register_user'),
    path('change_password/',views.change_password,name='change_password'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),

    path('create_schedule_curing/', views.create_schedule_curing, name='create_schedule_curing'),
    path('schedule_curing_table/<int:transaction_concreting_id>/', views.schedule_curing_table, name='schedule_curing_table'),
    path('create_project/', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('create_site/', views.create_site, name='create_site'),
    path('edit_site/<int:site_id>/', views.edit_site, name='edit_site'),
    path('create_structural_element/', views.create_structural_element, name='create_structural_element'),
    path('edit_structural_element/<int:element_id>/', views.edit_structural_element, name='edit_structural_element'),

    path('transaction_concreting/', views.transaction_concreting_list, name='transaction_concreting_list'),
    # path('upload_image/', views.upload_image_view, name='upload_image'),
    path('get_sites_for_project/<int:project_id>/', views.get_sites_for_project, name='get_sites_for_project'),


    #Experiment
    path('camera/',exeriment.camera_view,name='camera_view' ), 
    path('exschedule_curing_table/<int:transaction_concreting_id>/', exeriment.schedule_curing_table, name='exschedule_curing_table'),
    path('upload_image/', exeriment.upload_image_view, name='upload_image'),
 
]