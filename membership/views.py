from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Membership


def all_memberships(request):

    """ A view to return the membership page """

    memberships = Membership.objects.all()

    content = {
        'memberships': memberships,
    }

    return render(request, 'membership/membership.html', content)


@login_required
def add_membership(request):

    """ Adds a membership offer to the store (superuser) """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do this.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save()
            messages.success(request, 'Successfully added new offer!')
            return redirect(reverse('offer_details', args=[offer.id]))
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
