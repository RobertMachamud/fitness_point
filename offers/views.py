from django.shortcuts import render
from .models import Offer


def all_offers(request):
    """ A view to show all offers, including search queries and sorting """

    offers = Offer.objects.all()

    content = {
        'offers': offers,
    }

    return render(request, 'offers/offers.html', content)
