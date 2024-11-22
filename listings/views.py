# listings/views.py
from rest_framework import generics, permissions, viewsets
from .models import Booking, Review, Listing
from .serializers import BookingSerializer, ReviewSerializer, ListingSerializer
from .permissions import IsLandlord, IsTenant
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import ListingForm,BookingForm
from django.http import HttpResponseForbidden
from django.http import HttpResponse # Форма для работы с объявлениями
from accounts.models import CustomUser  # Импорт модели пользователя

def home(request):
    return render(request, 'home.html')
# Для бронирований
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        # Присваиваем текущего пользователя как арендатора
        serializer.save(tenant=self.request.user)
class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsLandlord]
    def get_queryset(self):
        # разрешаем обновление бронирования
        if self.request.user.role == 'landlord':
            return Booking.objects.filter(listing__owner=self.request.user)
        return Booking.objects.none()
# Для отзывов
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        # присваиваем текущего пользователя
        serializer.save(tenant=self.request.user)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        # присваиваем текущего пользователя как владельца
        serializer.save(landlord=self.request.user)
    def get_queryset(self):
        # отображаем  объявления пользователю
        return Listing.objects.filter(landlord=self.request.user)
# Для моих
@login_required
def my_listings(request):
    listings = Listing.objects.filter(landlord=request.user)  # фильтруем объявления по пользователю
    return render(request, 'listings/my_listings.html', {'listings': listings})
# Для "Все объявления"
def all_listings(request):
    listings = Listing.objects.all()  # Все объявления на сайте
    return render(request, 'listings/all_listings.html', {'listings': listings})
# делаем новое объявления
@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.landlord = request.user  # Присваиваем текущего пользователя как владельца
            listing.save()
            return redirect('listings:my_listings')  # Перенаправляем на страницу "Мои объявления"
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})
# Для редактирования объявления
@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:view-listing', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/edit_listing.html', {'form': form, 'listing': listing})
# Для удаления объявления

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    # Проверка, является ли пользователь владельцем объявления
    if listing.landlord != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")
    if request.method == 'POST':
        listing.delete()
        return redirect('listings:my-listings')  # Убедитесь, что маршрут my-listings существует
    return render(request, 'listings/delete_listing.html', {'listing': listing})

# Для просмотра
@login_required
def view_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, landlord=request.user)
    return render(request, 'listings/view_listing.html', {'listing': listing})



# Представление для подтверждения бронирования арендодателем
class BookingConfirmView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        booking = super().get_object()
        if booking.listing.landlord != self.request.user:
            raise Http404("You are not the landlord of this listing.")
        return booking

    # Подтверждаем бронирование
    def perform_update(self, serializer):
        booking = self.get_object()
        booking.confirm()


# Представление для отклонения бронирования арендодателем
class BookingRejectView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        booking = super().get_object()
        if booking.listing.landlord != self.request.user:
            raise Http404("You are not the landlord of this listing.")
        return booking

    # Отклоняем бронирование
    def perform_update(self, serializer):
        booking = self.get_object()
        booking.reject()


#  создание бронирования
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        # Присваиваем текущего пользователя как арендатора
        serializer.save(tenant=self.request.user)
# Представление для отмены бронирования арендатора
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tenant=request.user)
    if not booking.can_cancel():
        return render(request, 'booking/cannot_cancel.html')
    booking.status = 'rejected'  # Отклоняем бронирование
    booking.save()
    return redirect('bookings:my_bookings')  # Перенаправление на страницу с бронированиями арендатора
# Представление для списка бронирований арендатора
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(tenant=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def view_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    # Получение всех бронирований для этого объявления
    bookings = Booking.objects.filter(listing=listing)
    # Проверка, есть ли подтвержденные бронирования
    booking_status = 'Забронировано' if bookings.filter(status='confirmed').exists() else 'Свободно'
    return render(request, 'listings/view_listing.html', {
        'listing': listing,
        'booking_status': booking_status,
    })

def book_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.user = request.user
            booking.save()
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = BookingForm()
    return render(request, 'book_listing.html', {'listing': listing, 'form': form})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # Проверка, чтобы указанные даты не пересекались с другими бронированиями
            # Можно сделать фильтрацию на основе модели Booking
            if listing.available:  # Проверка, доступно ли объявление для бронирования
                # Создаем бронирование
                listing.available = False  # Обновляем статус объявления на "занято"
                listing.save()

                return redirect('booking_success')
            else:
                #  показываем ошибку
                form.add_error(None, 'This listing is no longer available for booking.')
    else:
        form = BookingForm()
    return render(request, 'listings/listing_detail.html', {'listing': listing, 'form': form})

def booking_success(request):
    return HttpResponse("Your booking was successful!")

class DeleteListingView(View):
    def get(self, request, pk):

        # Получаем объявление по id (pk)
        listing = get_object_or_404(Listing, pk=pk)
        # Отображаем страницу подтверждения удаления
        return render(request, 'listings/delete_listing.html', {'listing': listing})
    def post(self, request, pk):
        # Получаем объявление по id (pk)
        listing = get_object_or_404(Listing, pk=pk)
        # Удаляем объявление
        listing.delete()
        # Перенаправляем на страницу со списком объявлений
        return redirect('listings:my-listings')

    # listings/views.py
    from django.shortcuts import get_object_or_404, redirect
    from django.views import View
    from .models import Listing, Booking
    class BookingCreateView(View):
        def get(self, request, listing_id):
            # Получаем объявление по ID
            listing = get_object_or_404(Listing, id=listing_id)
            # Проверяем, что объявление доступно для бронирования
            if listing.booking_status != "Open":
                # Если объявление недоступно для бронирования, перенаправляем
                return redirect('listings:listing-detail', listing_id=listing.id)
                # Создаем бронирование
            booking = Booking.objects.create(listing=listing, user=request.user)
            # Обновляем статус объявления на "Забронировано"
            listing.booking_status = "Booked"
            listing.save()
            # Перенаправляем на страницу с успешным бронированием или на страницу объявления
            return redirect('listings:listing-detail', listing_id=listing.id)


# Страница просмотра объявления и бронирования
@login_required
def view_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if not listing.is_available():
        return render(request, 'listings/view_listing.html', {
            'listing': listing,
            'error': 'Это объявление не доступно для бронирования.',
        })
    booking_form = BookingForm()
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            start_date = booking_form.cleaned_data['start_date']
            end_date = booking_form.cleaned_data['end_date']
            # Проверка на пересечение с существующими бронированиями
            overlapping_bookings = Booking.objects.filter(
                listing=listing,
                status='confirmed',
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            if overlapping_bookings.exists():
                return render(request, 'listings/view_listing.html', {
                    'listing': listing,
                    'booking_form': booking_form,
                    'error': 'Эти даты уже забронированы.',
                })
            # Создание бронирования
            booking = booking_form.save(commit=False)
            booking.listing = listing
            booking.tenant = request.user
            booking.save()
            return redirect('listings:my_bookings')
    return render(request, 'listings/view_listing.html', {
        'listing': listing,
        'booking_form': booking_form,
    })
# Страница для управления бронированиями арендодателем
@login_required
def manage_bookings(request):
    listings = Listing.objects.filter(landlord=request.user)
    bookings = Booking.objects.filter(listing__in=listings, status='pending')
    return render(request, 'listings/manage_bookings.html', {'bookings': bookings})
# Подтверждение бронирования
@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.confirm()
    return redirect('listings:manage_bookings')
# Отклонение бронирования
@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.reject()
    return redirect('listings:manage_bookings')

def view_listing(request, pk):
    # Получаем объект объявления по pk
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/view_listing.html', {'listing': listing})

@login_required
def manage_booking(request, pk, action):
    listing = get_object_or_404(Listing, pk=pk)
    # Проверяем, что текущий пользователь — владелец объявления
    if listing.owner != request.user:
        return HttpResponseForbidden("У вас нет прав управлять этим объявлением.")
    if action == 'approve':
        listing.booking_status = 'approved'
        listing.is_booked = True
    elif action == 'reject':
        listing.booking_status = 'rejected'
        listing.is_booked = False
    listing.save()
    return redirect('listings:my-listings')  # Возврат к списку объявлений владельца

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
@login_required
def manage_booking(request, pk, action):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.owner != request.user:
        return HttpResponseForbidden("У вас нет прав управлять этим объявлением.")
    if action == 'approve':
        listing.booking_status = 'approved'
        listing.is_booked = True
    elif action == 'reject':
        listing.booking_status = 'rejected'
        listing.is_booked = False
    listing.save()
    return redirect('listings:my-listings')  # Возврат к списку объявлений владельца
