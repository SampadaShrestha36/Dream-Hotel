from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Room)
admin.site.register(Gallery)
admin.site.register(Booking)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(GuestProfile)
admin.site.register(Payment)