from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# Create your views here.
from udachi.forms import OstavitOtzivForm, BronirovanieForm
from udachi.models import Bluda, Otzivi, TipBluda
from cart.forms import CartAddBludaForm


class NewsDetailView(DetailView):
    model = Bluda
    template_name = 'udachi/detail_view.html'
    context_object_name = 'bluda'

def render_page_home(request, alert=None):
    bluda_iz_topa = Bluda.objects.order_by('kolvo_dobavlenia_v_korzinu')[0:6]

    otzivi = Otzivi.objects.filter(prosli_moderaziu=True).order_by('data_otziva')

    forma_ostavit_otziv = OstavitOtzivForm()

    return render(request, 'udachi/home.html', {
        'bluda_iz_topa': bluda_iz_topa,
        'otzivi': otzivi,
        'forma_ostavit_otziv': forma_ostavit_otziv,
        'alert': alert
    })


def render_page_bluda_lv(request, vid):
    bluda = Bluda.objects.filter(ne_pokazivat=False)
    tip_bluda = TipBluda.objects.filter(id=vid)

    return render(request, 'udachi/bluda_lv.html', {
        'bluda': bluda,
        'tip_bluda': tip_bluda,
        'vid': vid
    })

def otziv(request, alert=None):
    forma_ostavit_otziv = OstavitOtzivForm()
    otzivi = Otzivi.objects.filter(prosli_moderaziu=True).order_by('data_otziva')
    return render(request, 'udachi/otziv.html', {
        'forma_ostavit_otziv': forma_ostavit_otziv,
        'alert': alert,
        'otzivi': otzivi,
    })

def product_detail(request, id, slug):
    bluda = get_object_or_404(Bluda,
                                id=id,
                                slug=slug,
                                available=True)
    cart_bluda_form = CartAddBludaForm()
    return render(request, 'udachi/detail_view.html', {'bluda': bluda,
                                                        'cart_bluda_form': cart_bluda_form})

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
    return render(request, 'udachi/bronirovanie.html', {'form' : form})


    # # РАБОТА С КОРЗИНОЙ
    #
    # @require_POST
    # def cart_add(request, bluda_id):
    #     cart = Cart(request)
    #     bluda = get_object_or_404(Bluda, id=bluda_id)
    #     form = CartAddBludaForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         cart.add(bluda=bluda,
    #                  quantity=cd['quantity'],
    #                  update_quantity=cd['update'])
    #     return redirect('cart : cart_detail')
    #
    #
    # def cart_remove(request, bluda_id):
    #     cart = Cart(request)
    #     bluda = get_object_or_404(Bluda, id=bluda_id)
    #     cart.remove(bluda)
    #     return redirect('cart : cart_detail')
    #
    #
    # def cart_detail(request):
    #     cart = Cart(request)
    #     return render(request, 'cart/detail.html', {'cart': cart})