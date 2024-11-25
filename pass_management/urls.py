from django.contrib import admin
from django.urls import path, include
from pass_management import views 

urlpatterns = [


   
    path('', views.index ,name="home" ),
    path('login/', views.login ,name="login" ),
    path('viewpass/', views.view_pass, name='pass_Enquiry'),
    path('view_PassEnquiryDtls/<int:pid>', views.PassEnquiryDtls, name='view_PassEnquiryDtls'),
    path('dashborad/', views.dashborad ,name="dashboard" ),
    path('user_dashboard/', views.user_dashborad ,name="dashboard" ),
    path('purchase_pass/', views.purchase_pass ,name="purchase_pass" ),
    path('add_category/', views.add_category ,name="add_category" ),
    path('manage_category/', views.manage_category ,name="manage_category" ),
    path('edit_Category/<int:pid>', views.edit_Category ,name="edit_Category" ),
    path('delete_Category/<int:pid>', views.delete_Category ,name="delete_Category" ),
    path('add_pass/', views.add_pass,name="add_pass" ),
    path('manage_pass/', views.manage_pass ,name="manage_pass" ),
    path('edit_pass/<int:pass_id>/', views.edit_pass, name='edit_pass'),

    path('delete_pass/<int:pid>', views.delete_pass ,name="delete_pass" ),
    path('read_queries/', views.read_queries ,name="read_queries" ),
    path('mange_queries/', views.mange_queries ,name="mange_queries" ),
    path('contact/', views.contact ,name="contact" ),
    path('about/', views.about ,name="about" ),
    path('signup/', views.Signup.as_view() ,name="signup" ),
    path('logout/', views.logoutUser ,name="logout" ),
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/add/', views.LocationCreateView.as_view(), name='location_add'),
    path('locations/edit/<int:pk>/', views.LocationUpdateView.as_view(), name='location_edit'),
    path('locations/delete/<int:pk>/', views.LocationDeleteView.as_view(), name='location_delete'),

    path('get_cost/', views.get_cost, name='get_cost'),
    path('purchase-pass/', views.purchase_pass, name='purchase_pass'),
    path('payment/success/', views.payment_success, name='payment_success'),

    path('routecosts/', views.RouteCostListView.as_view(), name='routecost_list'),
    path('routecosts/add/', views.RouteCostCreateView.as_view(), name='routecost_add'),
    path('routecosts/edit/<int:pk>/', views.RouteCostUpdateView.as_view(), name='routecost_edit'),
    path('routecosts/delete/<int:pk>/', views.RouteCostDeleteView.as_view(), name='routecost_delete'),
]
