from django.shortcuts import render


def index(request):
    """ A view to return the index/landing page """

    return render(request, 'home/index.html')
