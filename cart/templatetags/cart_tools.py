from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, qty):
    return price * qty


@register.filter(name='member_discount')
def member_discount(price, discount):
    d_price = float(price - (price / 100 * discount))
    discounted = "{:.2f}".format(d_price)
    return discounted


@register.simple_tag(name='calc_disc_subtotal')
def calc_disc_subtotal(price, discount, qty):
    disc = float((price - (price / 100 * discount)) * qty)
    discounted = "{:.2f}".format(disc)
    return discounted
