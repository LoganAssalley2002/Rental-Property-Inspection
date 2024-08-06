from django.urls import path

from core import views


urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('account/', views.account, name='account'),

    path('account/inspections/', views.inspections, name='inspections'),
    path('account/properties/', views.properties, name='properties'),
    path('account/properties/create/', views.create_property, name='create_property'),
    path('account/properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('account/inspections/create/', views.create_inspection, name='create_inspection'),
    path('account/inspections/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),
    path('account/inspections/<int:inspection_id>/property/', views.create_inspection_property, name='create_inspection_property'),
    path('account/inspections/<int:inspection_id>/add-area/', views.create_inspection_area, name='create_inspection_area'),
    path('account/inspections/<int:inspection_id>/areas/<int:area_id>/', views.area_detail, name='area_detail'),
]