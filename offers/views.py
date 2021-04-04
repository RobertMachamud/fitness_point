from django.shortcuts import render
from .models import Offer


def index(request):
    """ A view to show all offers, including search queries and sorting """

    offers = Offer.objects.all()

    context = {
        'offers': offers,
    }

    return render(request, 'offers/offers.html', context)
