from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.decorators.http import require_POST

# Create your views here.
from udachi.forms import OstavitOtzivForm, BronirovanieForm, ZakazCreateForm
from udachi.models import Bluda, Otzivi, TipBluda, DetaliZakaza
from udachi.forms import CartAddBludaForm
from udachi.cart import Cart


# РАБОТА С КОРЗИНОЙ
@require_POST
def cart_add(request, bluda_id):
    cart = Cart(request)
    bluda = get_object_or_404(Bluda, id=bluda_id)
    form = CartAddBludaForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(Bluda=bluda,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, bluda_id):
    cart = Cart(request)
    bluda = get_object_or_404(Bluda, id=bluda_id)
    cart.remove(bluda)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'udachi/detail.html', {'cart': cart})


# Рендеринг страниц

class NewsDetailView(DetailView):
    model = Bluda
    template_name = 'udachi/detail_view.html'
    context_object_name = 'bluda'


def render_page_home(request, alert=None):
    bluda_iz_topa = Bluda.objects.order_by('kolvo_dobavlenia_v_korzinu')[0:6]

    otzivi = Otzivi.objects.filter(prosli_moderaziu=True).order_by('data_otziva')
    cart_bluda_form = CartAddBludaForm()
    forma_ostavit_otziv = OstavitOtzivForm()

    return render(request, 'udachi/home.html', {
        'bluda_iz_topa': bluda_iz_topa,
        'otzivi': otzivi,
        'forma_ostavit_otziv': forma_ostavit_otziv,
        'alert': alert,
        'cart_bluda_form': cart_bluda_form
    })


def render_page_bluda_lv(request, vid):
    bluda = Bluda.objects.filter(ne_pokazivat=False)
    tip_bluda = TipBluda.objects.filter(id=vid)
    cart_bluda_form = CartAddBludaForm()

    return render(request, 'udachi/bluda_lv.html', {
        'bluda': bluda,
        'tip_bluda': tip_bluda,
        'vid': vid,
        'cart_bluda_form': cart_bluda_form
    })


def otziv(request, alert=None):
    forma_ostavit_otziv = OstavitOtzivForm()
    otzivi = Otzivi.objects.filter(prosli_moderaziu=True).order_by('data_otziva')
    return render(request, 'udachi/otziv.html', {
        'forma_ostavit_otziv': forma_ostavit_otziv,
        'alert': alert,
        'otzivi': otzivi,
    })


def ostavit_otziv(request):
    if request.method == "POST":
        form = OstavitOtzivForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            # post.save()
            form.save(commit=True)

            # mail_title = 'Test Email'
            # message = 'This is a test email.'
            # email = settings.DEFAULT_FROM_EMAIL
            # recipients = ['udachikafe75@gmail.com',]
            #
            # try:
            #     send_mail(mail_title, message, email, recipients, settings.EMAIL_HOST_USER,
            #               settings.EMAIL_HOST_PASSWORD)
            return otziv(request, alert='Ваш отзыв успешно отправлен')

        else:
            return otziv(request, alert='По')
    else:
        return otziv(request, alert='Это не POST!')


def contacts(request):
    return render(request, 'udachi/contacts.html')


def bronirovanie(request):
    error: ''
    if request.method == 'POST':
        form = BronirovanieForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            error = 'Заявка отправлена, оператор позвонит вам для подтверждения'
        else:
            error = 'Форма заполнена неверно'

    form = BronirovanieForm()
    return render(request, 'udachi/bronirovanie.html', {'form': form})


def zakaz_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = ZakazCreateForm(request.POST)
        if form.is_valid():
            zakaz = form.save()
            for item in cart:
                DetaliZakaza.objects.create(zakaz=zakaz,
                                    bluda=item['bluda'],
                                    stoimost_na_moment_realizazii=item['price'],
                                    kolvo=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'udachi/created.html',
                          {'zakaz': zakaz})
    else:
        form = ZakazCreateForm
    return render(request, 'udachi/create.html',
                  {'cart': cart, 'form': form})
