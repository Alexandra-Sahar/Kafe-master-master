from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render

# Create your views here.
from kafe import settings
from udachi.forms import OstavitOtzivForm
from udachi.models import Bluda, Otzivi


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


def render_page_bluda_lv(request):
    bluda = Bluda.objects.filter(ne_pokazivat=False)

    return render(request, 'udachi/bluda_lv.html', {
        'bluda': bluda
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
            return render_page_home(request, alert='Успех')




        else:
            return render_page_home(request, alert='Заполняй правильно!')
    else:
        return render_page_home(request, alert='Это не POST!')
