from django.shortcuts import render


def user_profile(request):

    """ Displays the user's profile """

    template = 'user_profiles/user_profile.html'
    content = {}

    return render(request, template, content)
