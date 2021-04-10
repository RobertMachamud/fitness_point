
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def user_profile(request):

    """ Displays the user's profile. """

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = user_profile.orders.all()

    template = 'user_profiles/user_profile.html'
    content = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, content)