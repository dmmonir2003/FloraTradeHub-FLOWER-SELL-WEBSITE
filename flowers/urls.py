from django.urls import path
from .views import CreateFlowerCategoryView, CreateFlowerView, AddOrder, CartView, UpdateFlowerView, FlowerDeshbordView, DeleteFlowerView, OrderDeshbordView, OrderConfirmView, RemoveOrderToCart
urlpatterns = [
    path('create-category/', CreateFlowerCategoryView.as_view(), name='add_category'),
    path('create-flower/', CreateFlowerView.as_view(), name='add_flower'),
    path('update_flower/<int:pk>/',
         UpdateFlowerView.as_view(), name='update_flower'),
    path('delete_flower/<int:pk>/',
         DeleteFlowerView.as_view(), name='delete_flower'),

    path('order/<int:flower_id>/', AddOrder, name='add_order'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('flower_deshbord/', FlowerDeshbordView.as_view(),
         name='flower_deshbord_view'),
    path('order_deshbord/', OrderDeshbordView.as_view(),
         name='order_deshbord'),
    path('order_confirm/<int:order_id>/', OrderConfirmView,
         name='order_confirm'),
    path('order_remove_to_cart/<int:order_id>/', RemoveOrderToCart,
         name='order_remove_to_cart'),

]
