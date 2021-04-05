from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Offer


def all_offers(request):

    """ A view to show all offers, including search queries and sorting """

    search_query = None
    offers = Offer.objects.all()

    if request.GET:
        if 'q' in request.GET:
            search_query = request.GET['q']
            if not search_query:
                messages.error(request, "You need to enter a search criteria.")
                return redirect(reverse('offers'))

            queries_to_search = Q(name__icontains=search_query) | Q(descr__icontains=search_query)
            offers = offers.filter(queries_to_search)

    content = {
        'offers': offers,
        'to_search': search_query,
    }

    return render(request, 'offers/offers.html', content)


def offer_details(request, offer_id):

    """ A view to show individual details from each offer """

    offer = get_object_or_404(Offer, pk=offer_id)

    content = {
        'offer': offer,
    }

    return render(request, 'offers/offer_details.html', content)
