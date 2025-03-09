from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('change_status/<int:order_id>/', views.update_order, name='update_order'),
    path('revenue/', views.revenue_for_shift, name='revenue'),
    path('api/', include(router.urls))
]

