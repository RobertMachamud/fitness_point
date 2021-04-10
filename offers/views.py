from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Offer, Category
from django.db.models.functions import Lower
from .forms import OfferForm


def all_offers(request):

    """ A view to show all offers, including search queries and sorting """
    sorting = None
    search_query = None
    sorting_direction = None
    categories_to_search = None
    offers = Offer.objects.all()

    if request.GET:
        if 'q' in request.GET:
            search_query = request.GET['q']
            if not search_query:
                messages.error(request, "You need to enter a search criteria.")
                return redirect(reverse('offers'))

            queries_to_search = Q(name__icontains=search_query) | Q(descr__icontains=search_query)
            offers = offers.filter(queries_to_search)

        if 'sort' in request.GET:
            sort_key = request.GET['sort']
            sorting = sort_key
            if sort_key == 'name':
                sort_key = 'lower_name'
                offers = offers.annotate(lower_name=Lower('name'))
            if sort_key == 'category':
                sort_key = 'category__name'

            if 'direction' in request.GET:
                sorting_direction = request.GET['direction']
                if sorting_direction == 'desc':
                    sort_key = f'-{sort_key}'
            offers = offers.order_by(sort_key)

        if 'category' in request.GET:
            categories_to_search = request.GET['category'].split(',')
            offers = offers.filter(category__name__in=categories_to_search)
            categories_to_search = Category.objects.filter(
                name__in=categories_to_search)

    curr_sorting = f'{sorting}_{sorting_direction}'

    content = {
        'offers': offers,
        'to_search': search_query,
        'curr_sorting': curr_sorting,
        'curr_categories': categories_to_search,
    }
    return render(request, 'offers/offers.html', content)


def offer_details(request, offer_id):

    """ A view to show individual details from each offer """

    offer = get_object_or_404(Offer, pk=offer_id)

    content = {
        'offer': offer,
    }
    return render(request, 'offers/offer_details.html', content)


def add_offer(request):

    """ Adds an offer to the store """

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added new offer!')
            return redirect(reverse('add_offer'))
        else:
            messages.error(
                request, 'Failed to add the offer. \
                Please ensure the form is valid.')
    else:
        form = OfferForm()

    template = 'offers/add_offer.html'
    content = {
        'form': form,
    }
    return render(request, template, content)


def upd_offer(request, offer_id):

    """ Edits an offer in the store """

    offer = get_object_or_404(Offer, pk=offer_id)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated the offer!')
            return redirect(reverse('offer_detail', args=[offer.id]))
        else:
            messages.error(
                request, 'Failed to update the offer. \
                Please ensure the form is valid.')
    else:
        form = OfferForm(instance=offer)
        messages.info(request, f'You are updating: {offer.name}')

    template = 'offers/upd_offer.html'
    content = {
        'form': form,
        'offer': offer,
    }
    return render(request, template, content)
