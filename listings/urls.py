# listings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingCreateView, BookingUpdateView, ReviewListCreateView
from . import views
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
urlpatterns = [
    # API маршруты
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings/<int:pk>/', BookingUpdateView.as_view(), name='update-booking'),
    path('reviews/', ReviewListCreateView.as_view(), name='reviews'),
    # Основные маршруты для listings
    path('', include(router.urls)),  # Включение маршрутов
    path('my-listings/', views.my_listings, name='my_listings'),
    path('my-listings/', views.my_listings, name='my-listings'),
    # Мои объявления
    path('all-listings/', views.all_listings, name='all_listings'),  # Все объявления
    path('create/', views.create_listing, name='create'),  # Создание объявления
    path('update/<int:pk>/', views.edit_listing, name='update-listing'),  # Редактирование
    path('delete/<int:pk>/', views.delete_listing, name='delete-listing'),  # Удаление
    path('<int:pk>/', views.view_listing, name='view-listing'),  # Просмотр объявления
    # Ссылки для бронирования
    path('bookings/confirm/<int:pk>/', views.BookingConfirmView.as_view(), name='confirm-booking'),
    path('bookings/reject/<int:pk>/', views.BookingRejectView.as_view(), name='reject-booking'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel-booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),  # Список бронирований арендатора
    path('booking_success/', views.booking_success, name='booking_success'),
    path('', views.all_listings, name='all-listings'),  # маршрут для всех
    path('listing/<int:pk>/', views.view_listing, name='view-listing'),
    path('<int:pk>/manage-booking/<str:action>/', views.manage_booking, name='manage-booking'),

]
app_name = 'listings'