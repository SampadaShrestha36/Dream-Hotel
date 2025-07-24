from .models import GuestProfile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = GuestProfile.objects.get(user=request.user)
            return {'profile': profile}
        except GuestProfile.DoesNotExist:
            return {'profile': None}
    return {}
