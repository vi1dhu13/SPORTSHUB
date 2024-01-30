from django.urls import path
from . import views
from .views import sports_center_list,add_center
from .views import SportsCenterListView

urlpatterns = [
    path("", views.index, name='index'),
    path('services/', sports_center_list, name='services'),
    path('add-center/', add_center, name='add_center'),
  
    path('sports-centers/', SportsCenterListView.as_view(), name='sports_center_list'),

    path('sports-center/<int:sports_center_id>/select-slot/', views.select_slot, name='select_slot'),
    path('sports-center/<int:sportscenter_id>/get-available-slots/<str:selected_date>/', views.get_available_slots, name='get_available_slots'),
    # path('payment/', views.payment, name='payment'),
    path('payment/reservation/<int:reservation_id>/', views.payment, name='payment_reservation'),

    # URL for payment with assignment_id
    path('payment/assignment/<int:assignment_id>/', views.payment, name='payment_assignment'),
    path('paymenthandler/<int:reservation_id>/', views.paymenthandler, name='paymenthandler_reservation'),
    path('paymenthandler/assignment/<int:assignment_id>/', views.paymenthandler, name='paymenthandler_assignment'),
    
    path('paymenthandler/<int:reservation_id>/', views.paymenthandler, name='paymenthandler'),
    


]
# urls.py
