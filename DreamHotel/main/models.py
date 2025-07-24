from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures',null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.user.username
class Room(models.Model):
    ROOM_TYPES = [('single', 'Single'), ('double', 'Double'), ('triple', 'triple')]
    title=models.TextField(default="null")
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    total_rooms = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    images=models.ImageField(default=" ",upload_to='images')
    image2=models.ImageField(default=" ",upload_to='images')
    image3=models.ImageField(default=" ",upload_to='images')
    image4=models.ImageField(default=" ",upload_to='images')

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile",null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    number_of_guests=models.PositiveIntegerField(null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booked_rooms = models.PositiveIntegerField(default=1)  # Number of rooms booked in this booking
    total_nights=models.PositiveBigIntegerField(null=True)
    total_price=models.PositiveBigIntegerField(null=True)
    def __str__(self):
        return f"Booking of {self.booked_rooms} room(s) of {self.room.title}"

class Message(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.EmailField()
    phonenumber=PhoneNumberField(blank=True,region='NP')
    message=models.TextField()

class Gallery(models.Model):
    title=models.TextField(default="null")
    images=models.ImageField(default=" ",upload_to='images')

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('Khalti', 'Khalti'), ('e-Sewa', 'e-Sewa'), ('cash', 'Cash')])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.amount_paid}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="reviews",null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews",null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews",null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username if self.user else 'Anonymous'} for {self.room.title}"
