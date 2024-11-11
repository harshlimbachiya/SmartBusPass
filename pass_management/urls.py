from django.contrib import admin
from django.urls import path, include
from pass_management import views 

urlpatterns = [
    path('', views.index ,name="home" ),
    path('login/', views.login ,name="login" ),
    path('dashborad/', views.dashborad ,name="dashboard" ),
    path('user_dashboard/', views.user_dashborad ,name="dashboard" ),
    path('purchase_pass/', views.purchase_pass ,name="purchase_pass" ),
    path('add_category/', views.add_category ,name="add_category" ),
    path('manage_category/', views.manage_category ,name="manage_category" ),
    path('edit_Category/<int:pid>', views.edit_Category ,name="edit_Category" ),
    path('delete_Category/<int:pid>', views.delete_Category ,name="delete_Category" ),
    path('add_pass/', views.AddPass.as_view() ,name="add_pass" ),
    path('manage_pass/', views.manage_pass ,name="manage_pass" ),
    path('edit_pass/<int:pid>', views.edit_pass ,name="edit_pass" ),
    path('delete_pass/<int:pid>', views.delete_pass ,name="delete_pass" ),
    path('read_queries/', views.read_queries ,name="read_queries" ),
    path('mange_queries/', views.mange_queries ,name="mange_queries" ),
    path('contact/', views.contact ,name="contact" ),
    path('about/', views.about ,name="about" ),
    path('signup/', views.Signup.as_view() ,name="signup" ),
    path('logout/', views.logoutUser ,name="logout" )
]
