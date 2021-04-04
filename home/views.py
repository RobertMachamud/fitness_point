from django.shortcuts import render


def all_offers(request):
    """ A view to return the index/landing page """

    return render(request, 'home/index.html')
