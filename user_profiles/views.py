from django.shortcuts import render, get_object_or_404
from .models import UserProfile


def user_profile(request):

    """ Displays the user's profile """

    user_profile = get_object_or_404(UserProfile, user=request.user)

    template = 'user_profiles/user_profile.html'
    content = {
        'user_profile': user_profile,
    }

    return render(request, template, content)
