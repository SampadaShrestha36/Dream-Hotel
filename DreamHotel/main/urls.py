from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views    

urlpatterns = [
    path("", home, name="home"),
    path("contact/",contact,name="contact"),
    path("aboutus/",aboutus,name="aboutus"),
    path("gallery/",gallery,name="gallery"),
    path("rooms/",rooms,name="rooms"),
    path("book/<int:room_id>",bookrooms,name="bookrooms"),
   
       # authorization
    path("register/",register,name="register"),
    path("login/",log_in,name="login"),
    path("logout/",log_out,name="logout"),
    path("change/",change_password,name="change_password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    path('user_information/',user_information,name="user_information"),
    path('reviews/<int:booking_id>/',reviews,name="reviews"),
    path('edit_reviews/<int:booking_id>/',edit_review,name="edit_review"),
    path('delete-review/<int:booking_id>/', delete_review, name='delete_review'),
     path('view_review/<int:booking_id>/', view_review, name='view_review'),
    path("edit_profile/",edit_profile,name="edit_profile"),
    path("delete_profile/",delete_profile,name="delete_profile"),
    # payment
    path("bookingconfirmation/<int:booking_id>/",bookingconfirmation,name="bookingconfirmation"),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path("paymentsuccess/<int:booking_id>/",paymentsuccess,name="paymentsuccess"),
    path('payment-ways/<int:booking_id>/', initiate_payment, name='initiate_payment'),
    path('payment/failed/', payment_failed, name='payment_failed'),

]