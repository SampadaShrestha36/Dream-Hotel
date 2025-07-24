from django.db.models import Sum
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.mail import EmailMessage,send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date
import hmac
import hashlib
import uuid
import base64
import requests
import json
from django.http import JsonResponse
# Create your views here.
def index(request):
    profile = GuestProfile.objects.get(user=request.user)
    return render(request,'base.html',{'profile':profile})
def home(request):
    return render(request,'main/home.html')
def contact(request):
    if request.method=='POST':
        data=request.POST
        fname=data['fname']
        lname=data['lname']
        email=data['email']
        phonenumber=data['number']
        msg=data['message']
        Message.objects.create(fname=fname,lname=lname,email=email,phonenumber=phonenumber,message=msg)
        subject="Thankyou for your message"
        message=render_to_string('main/message.html',{'fname':fname})
        from_email="dream.hotel4@gmail.com"
        recipient_list=[email]
        msg_email=EmailMessage(subject,message,from_email,recipient_list)
        msg_email.send(fail_silently=True)
    return render(request,'main/contactus.html')
def aboutus(request):
    return render(request,'main/aboutus.html')
def gallery(request):
    img=Gallery.objects.all()
    data=Room.objects.all()
    return render(request,'main/gallery.html',{'data':data,'img':img})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room



@login_required(login_url='login')
def rooms(request):
    # Get search query from GET parameters
    search_query = request.GET.get('search', '')

    if search_query:
        # If there's a search query, show all matching rooms regardless of type
        room_results = Room.objects.filter(title__icontains=search_query)
        context = {
            'room_results': room_results,
            'search_query': search_query
        }
    else:
        # If no search, show rooms separated by type as before
        single = Room.objects.filter(room_type='single')
        double = Room.objects.filter(room_type='double')
        triple = Room.objects.filter(room_type='triple')
        context = {
            'single': single,
            'double': double,
            'triple': triple,
            'search_query': search_query
        }
    
    return render(request, 'main/rooms.html', context)
@login_required(login_url='login')
def bookrooms(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    total_rooms = room.total_rooms  # Total rooms for this room type
    max_guests_per_room = room.max_guests  # Maximum guests allowed per room

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        booked_rooms = int(request.POST.get('booked_rooms', 0))
        number_of_guests = int(request.POST.get('guests', 0))
        total_price=request.POST.get('price')
        total_nights=request.POST.get('bookedrooms')
        # Validate guests and rooms logic
        if booked_rooms > number_of_guests:
            messages.success(request, "Each room must have at least one guest.")
            return render(request, 'main/bookrooms.html', {'room': room,})
        if number_of_guests > booked_rooms * max_guests_per_room:
            messages.success(request, f"A maximum of {max_guests_per_room} guests is allowed for {booked_rooms} room(s).")
            return render(request, 'main/bookrooms.html', {
                'room': room,})

        # Process dates
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Fetch overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in_date__lte=check_out,
            check_out_date__gte=check_in,
        ).aggregate(total_booked=models.Sum('booked_rooms'))['total_booked'] or 0

        print("Overlapping bookings:", overlapping_bookings)

        # Calculate available rooms
        available_rooms = total_rooms - overlapping_bookings
        print("Total rooms:", total_rooms)
        print("Available rooms:", available_rooms)

        if booked_rooms > available_rooms:
            return render(request, 'main/bookrooms.html', {
                'room': room,
                'error_message': f"Only {available_rooms} room(s) are available for the selected dates.",
            })

        # Save booking
        booking=Booking.objects.create(user=request.user,room=room, check_in_date=check_in, check_out_date=check_out, 
                          booked_rooms=booked_rooms, number_of_guests=number_of_guests,total_price=total_price,total_nights=total_nights)

        return redirect('bookingconfirmation', booking_id=booking.id)
    reviews=Review.objects.filter(room=room)

    return render(request, 'main/bookrooms.html', {'room': room,'reviews':reviews})
@login_required
def reviews(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    profile=GuestProfile.objects.get(user=request.user)
    
    
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        try:
            # Create a new review for this booking
            Review.objects.create(
                booking=booking,
                room=booking.room,
                user=booking.user,  # Adjust if `Customer` is a separate model
                rating=rating,
                comment=comment,
            )
            return redirect('user_information')  # Redirect after successful submission
        except :
            messages.error(request, 'You already have a review for this booking.')
            return redirect('edit_review', booking_id=booking.id)
    
    return render(request, 'main/review.html', {'booking': booking,'profile':profile})
def edit_review(request, booking_id): 
    booking = get_object_or_404(Booking, id=booking_id)
    review=Review.objects.get(booking=booking)
    profile=GuestProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        
        # update a new review for this booking
        booking = get_object_or_404(Booking, id=booking_id)
        review=Review.objects.filter(booking=booking)
        review.update(
    room=booking.room,
    user=booking.user,
    rating=rating,
    comment=comment
)
        return redirect('user_information')  # Redirect after successful submission
    
    return render(request, 'main/edit_review.html', {'booking': booking,'profile':profile,'review':review})
def delete_review(request, booking_id):
    # Get the booking associated with the review
    booking = Booking.objects.get( id=booking_id, user=request.user)
    
    # Find the review for this booking
    try:
        review = Review.objects.get(booking=booking)
        review.delete()
        messages.success(request, 'Your review has been deleted successfully.')
    except Review.DoesNotExist:
        messages.error(request, 'No review found to delete.')
    
    return redirect('user_information')
def view_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    review=Review.objects.get(booking=booking)
    profile=GuestProfile.objects.get(user=request.user)
    
    return render(request, 'main/view_review.html', {'booking': booking,'profile':profile,'review':review})
    # authorization
def register(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'This username already exists')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'This email already has an account')
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username,password=password)
                    GuestProfile.objects.create(user=User.objects.get(username=username))
                    messages.success(request,"Registered successfully")
                    return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                    return redirect('register')
        else:
            messages.error(request,"Your password and confirm passwords do not match")
            return redirect('register')
    return render(request, 'auth/register.html')
def log_in(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        remember_me = request.POST.get('remember_me')
       
        if not User.objects.filter(username=username):
            messages.error(request,"Username does not exist")
            return redirect('login')
        else:
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if remember_me:
                    request.session.set_expiry(12000000)
                else:
                    request.session.set_expiry(0)
                messages.success(request,"login successful")
                return redirect('home')
            else:
                messages.error(request,"Incorrect Password")
                return redirect('login')
    return render(request,'auth/login.html')
def log_out(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'auth/changepassword.html',{'form':form})
def user_information(request):
    user_bookings = Booking.objects.filter(user=request.user.id)
    reviews=Review.objects.filter(user=request.user)
    reviews_by_booking = {review.booking.id: review for review in reviews}
    profile = GuestProfile.objects.get(user=request.user)

    return render(request, 'main/user_information.html',{'bookings': user_bookings,'profile':profile,'reviews':reviews,'reviews_by_booking': reviews_by_booking})
def edit_profile(request):
    try:
        profile = GuestProfile.objects.get(user=request.user)
    except GuestProfile.DoesNotExist:
        profile = None

    users = request.user

    if request.method == "POST":
        user = request.POST.get('username')
        e_mail = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        # Check for username uniqueness
        if not User.objects.filter(id=users.id):
            if User.objects.get(username=user).exists():
                messages.error(request, 'This username already exists.')
                return redirect('edit_profile')

        # Check for email uniqueness
        if not User.objects.filter(id=users.id):
            if User.objects.get(email=e_mail).exists():
                messages.error(request, 'This email is already associated with another account.')
                return redirect('edit_profile')

        # Update user details
        users.username = user
        users.email = e_mail
        users.first_name = first_name
        users.last_name = last_name
        users.save()

        # Update or create profile
        if not profile:
            profile = GuestProfile.objects.create(user=users)

        profile.bio = bio
        if profile_image:
            profile.profile_picture = profile_image
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('user_information')

    return render(request, 'main/edit_profile.html', {'profile': profile, 'user': users})
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('home')
    return render(request, 'main/delete_account.html')
# payment
def bookingconfirmation(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    return render(request,'payment/payment_confirm.html',{'booking':booking})
def cancel_booking(request, booking_id):
    # Fetch the booking object or return a 404 if it doesn't exist
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Ensure only the user's booking can be canceled
    
    # Delete the booking
    booking.delete()
    
    # Provide user feedback
    messages.success(request, "Your booking has been successfully canceled.")
    send_mail(
    'Booking Canceled',
    f'Your booking for {booking.room} from {booking.check_in_date} to {booking.check_out_date} has been canceled.',
    'noreply@dreamhotel.com',
    [request.user.email],
)
    
    # Redirect to a relevant page, e.g., the booking history or home page
    return redirect('rooms')  # Replace with your desired URL name
def genSha256(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')

    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()

    # Convert the digest to a Base64-encoded string
    signature = base64.b64encode(digest).decode('utf-8')

    return signature
def initiate_payment(request, booking_id):
    # Example data
    booking=get_object_or_404(Booking,id=booking_id)
    amount = booking.total_price
    tax_amount = 0
    total_amount = amount + tax_amount
    transaction_uuid = str(uuid.uuid4())  # Generate unique UUID
    product_code = "EPAYTEST"
    success_url = f"http://127.0.0.1:8000/paymentsuccess/{booking_id}/?q={booking_id}"
    failure_url = "http://127.0.0.1:8000/payment/failed/"

    # Create the hash signature
    secret_key = "8gBm/:&EnhH.1/q"
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code=EPAYTEST"

    signature = genSha256(secret_key, data_to_sign)

    context = {
        'amount': amount,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid,
        'product_code': product_code,
        'success_url': success_url,
        'failure_url': failure_url,
        'signature': signature,
    }
    return render(request, 'payment/payment_ways.html', context)
def verify_payment(request):
    transaction_id = request.GET.get('q')  # Transaction ID from eSewa
    ref_id = request.GET.get('refId')  # Reference ID from eSewa

    url = "https://uat.esewa.com.np/epay/transrec"
    data = {
        'amt': "total_amount",  # Amount to verify
        'rid': ref_id,  # Reference ID
        'pid': transaction_id,  # Your transaction ID
        'scd': "merchant_code"  # Your merchant code
    }

    response = requests.post(url, data=data)
    if "Success" in response.text:
        return JsonResponse({"status": "Payment Verified"})
    return JsonResponse({"status": "Payment Verification Failed"})
def decode_base64(data):
    decoded_data = base64.b64decode(data).decode('utf-8')
    print(decoded_data)
    return json.loads(decoded_data)
def payment_failed(request):
    messages.error(request, "Payment failed. Please try again.")
    return redirect('rooms')
def paymentsuccess(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    payment_method='e-Sewa'
    amount_paid=booking.total_price
    payment_completed=False
    Payment.objects.create(booking=booking,payment_method=payment_method,amount_paid=amount_paid,payment_completed=payment_completed)
    User=request.user
    subject="Thankyou for booking!"
    message=render_to_string('payment/success.html',{'Booking':booking})
    from_email="dream.hotel4@gmail.com"
    recipient_list=[User.email]
    msg_email=EmailMessage(subject,message,from_email,recipient_list)
    msg_email.send(fail_silently=True)
    return render(request,'payment/payment_success.html',{'Booking':booking})