from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('upload-name/',views.upload_name,name='upload-name'),
    path('upload-details/',views.upload_details,name='upload-details'),
    path('search/',views.product_search,name='product_search'),
    
    
    ]
