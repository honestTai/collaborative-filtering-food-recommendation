from myapp import views
from django.urls import path

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('search_list/', views.search_list, name='search_list'),
    path('list/', views.list, name='list'),
    path('recommend/', views.recommend, name='recommend'),
    path('detail/<int:foodid>', views.detail, name='myapp_fooddetail'),
    path('add_comment/<int:foodid>/', views.add_comment, name='add_comment'),
    path('add_to_wishlist/<int:foodid>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:foodid>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('user_view/', views.user_view, name='user_view'),
    path('change_password/', views.change_password, name='change_password'),
    path('analysis/', views.analysis, name='analysis'),
    path('favorite/', views.favorite, name='favorite'),
]
