from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from udachi.models import Bluda
from udachi.cart import Cart
from .forms import CartAddBludaForm


@require_POST
def cart_add(request, bluda_id):
    cart = Cart(request)
    bluda = get_object_or_404(Bluda, id=bluda_id)
    form = CartAddBludaForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(bluda=bluda,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart : cart_detail')


def cart_remove(request, bluda_id):
    cart = Cart(request)
    bluda = get_object_or_404(Bluda, id=bluda_id)
    cart.remove(bluda)
    return redirect('cart : cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/../udachi/templates/udachi/detail.html', {'cart': cart})
