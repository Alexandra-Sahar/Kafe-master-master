from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail


class TipBluda(models.Model):
    class Meta:
        verbose_name = 'Тип блюда'
        verbose_name_plural = 'Типы блюда'

    nazvanie = models.CharField(verbose_name='Название', max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nazvanie


class Bluda(models.Model):
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    nazvanie = models.CharField(verbose_name='Название', max_length=255, null=False, blank=False)
    opisanie = models.TextField('Описание', null=True, blank=True)
    cena = models.FloatField('Цена', default=0)
    gramovka = models.FloatField('Граммовка', default=0)
    prevyu = models.ImageField('Превью', null=False, blank=False)
    tip_bluda = models.ForeignKey(TipBluda, verbose_name='Тип блюда', on_delete=models.SET_NULL, null=True)
    ne_pokazivat = models.BooleanField('Не показывать блюдо', default=False)
    kolvo_dobavlenia_v_korzinu = models.IntegerField('Кол-во раз добавили в корзину', default=0)

    def __str__(self):
        return self.nazvanie


class Ingridienti(models.Model):
    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    nazvanie = models.CharField(verbose_name='Название', max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nazvanie


class IngridientiVBlude(models.Model):
    class Meta:
        verbose_name = 'Ингридиент в блюде'
        verbose_name_plural = 'Ингридиенты в блюде'

    ingridient = models.ForeignKey(Ingridienti, verbose_name='Ингридиенты', on_delete=models.SET_NULL, null=True)
    bludo = models.ForeignKey(Bluda, verbose_name='Блюда', on_delete=models.SET_NULL, null=True)
    gramovka = models.FloatField('Граммовка', )

class Bronirovanie(models.Model):
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    data = models.DateTimeField('Дата', null=True, blank=True)
    telephone = models.CharField('Tелефон', null=False, blank=False, max_length=255, )
    fio = models.CharField('ФИО', null=True, blank=True, max_length=255, )
    status_bronirovania = models.BooleanField('Бронь  подтверждена', default=False)
    predoplata = models.BooleanField('Предоплата', default=False)
    kolvo_gostei = models.IntegerField('Количество гостей', null=True, blank=True)
    stolik = models.IntegerField('Номер столика', null=True, blank=True, )

class Zakaz(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    sposob_otdachi = models.IntegerField(verbose_name='Способ отдачи', choices=(
        (1, 'Самовывоз'),
        (2, 'Доставка курьером'),
        (3, 'На месте'),
    ))

    telephone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Телефон')
    fio = models.CharField('ФИО', max_length=255, null=True, blank=True)
    data_i_vremia_zakaza = models.DateTimeField('Время заказа', auto_now_add=True, editable=False)
    adres = models.CharField('Адрес', max_length=255, null=True, blank=True, )
    zakaz_proveden = models.BooleanField('Заказ проведен', null=True, blank=True, )
    email = models.EmailField('Электронная почта', null=False, blank=False, default='kafeudachismolenka@gmail.com')
    bronirovanie = models.CharField('Бронирование', max_length=20, null=True, blank=True )

    def __str__(self):
        return f'#{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class DetaliZakaza(models.Model):
    class Meta:
        verbose_name = 'Деталь заказа'
        verbose_name_plural = 'Детали заказа'

    zakaz = models.ForeignKey(Zakaz, verbose_name='Заказ', on_delete=models.CASCADE)
    bludo = models.ForeignKey(Bluda, verbose_name='Блюдо', null=True, blank=True, on_delete=models.SET_NULL)
    kolvo = models.FloatField('Кол-во', default=1)
    stoimost_na_moment_realizazii = models.FloatField('Цена на момент реализации', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.stoimost_na_moment_realizazii * self.kolvo




class Sklad(models.Model):
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    nazvanie = models.CharField('Название склада', max_length=255)

    def __str__(self):
        return self.nazvanie


class IngridientiNaSklade(models.Model):
    class Meta:
        verbose_name = 'Ингридиент на складе'
        verbose_name_plural = 'Ингридиенты на складе'

    ingridient = models.ForeignKey(Ingridienti, verbose_name='Ингридиент', on_delete=models.CASCADE)
    sklad = models.ForeignKey(Sklad, verbose_name='Склад', on_delete=models.CASCADE)
    kolvo = models.FloatField('Кол-во', default=0)


class IstoriaizmeneniaNaSkladax(models.Model):
    class Meta:
        verbose_name = 'История измененения на складе'
        verbose_name_plural = 'Истории измененения на складе'

    tip_operazii = models.IntegerField('Тип операции', default=1, choices=(
        (1, 'Поступление'),
        (2, 'Спиисание'),
        (3, 'Реализация'),
        (4, 'Перемещение'),
    ))

    data_i_vremia = models.DateTimeField('Дата и время операции', auto_now_add=True)
    ispolnitel = models.ForeignKey(User, verbose_name='Исполнитель', on_delete=models.SET_NULL, null=True, blank=True)
    ingridient = models.ForeignKey(Ingridienti, verbose_name='Ингридиент', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    kolvo = models.FloatField('Кол-во', default=0)
    cena_na_moment_zakupki = models.FloatField('Цена на момент закупки', null=True, blank=True)
    sklad_otkuda = models.ForeignKey(Sklad, verbose_name='Склад откуда',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='sklad_otkuda_istoria'
                                     )

    sklad_kuda = models.ForeignKey(Sklad,
                                   verbose_name='Склад куда',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='sklad_kuda_istoria',
                                   blank=True)


class Postavshiki(models.Model):
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    naimenovanie = models.CharField(max_length=255, verbose_name='Наименование')
    telephone = models.CharField('Tелефон', null=True, blank=True, max_length=255)
    email = models.EmailField('Электронная почта', null=False, blank=False, default='kafeudachismolenka@gmail.com')
    adres = models.CharField('Адрес', null=True, blank=True, max_length=255)
    opisanie = models.TextField('Описание', null=True, blank=True)
    inn = models.CharField('ИНН', null=True, blank=True, max_length=255)

    def __str__(self):
        return self.naimenovanie


# class Sotrudnic(models.Model):
#     class Meta:
#         verbose_name = 'Сотрудник'
#         verbose_name_plural = 'Сотрудники'
#
#     user = models.OneToOneField(User, verbose_name='Логин', on_delete=models.CASCADE)
#     telephone = models.CharField('Tелефон', null=True, blank=True, max_length=255)
#     data_rozdenia = models.DateField('Дата рождения', null=True, blank=True)


class Otzivi(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    avtor = models.CharField('Автор', max_length=255)
    otziv = models.TextField('Отзыв')
    telephone_avtora = models.CharField('Телефон автора', max_length=255)
    data_otziva = models.DateTimeField('Дата', auto_now_add=True)
    prosli_moderaziu = models.BooleanField('Модерацию прошли', default=False)

    def get_short_opisanie(self):
        return self.otziv[0:100]

    def __str__(self):
        return f'{self.avtor}: {self.otziv[0:100]}...'


class Zayavka(models.Model):
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    postavshik = models.ForeignKey(Postavshiki, verbose_name='Поставщик', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    data = models.DateTimeField('Дата', auto_now_add=True)
    status = models.IntegerField('Тип операции', default=1, choices=(
        (1, 'Не Выполнено'),
        (2, 'Выполнено'),
    ))
    ispolnitel = models.ForeignKey(User, verbose_name='Исполнитель', on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return f'#{self.id}'

    # save() missing 1 required positional argument: 'send_mail'
    # def save(self, send_mail, **kwargs):
    #     self.send_mail(
    #         'Вам отправлена заявка как поставщику',
    #         'текст письма',
    #         settings.EMAIL_HOST_USER,
    #         [settings.EMAIL_HOST_USER]
    #                    )
    #     return JsonResponse({'status' : 'ok'})

    # def save(self):
    #
    #
    #     instance = super(Zayavka, self).save()
    #     for i in self.detalizayavki_set.all():
    #         print(i)
    #     self.send_email()
    #     return instance


    # def save_model(self, request, obj, form, change):
    #
    #     detali = DetaliZayavki.objects.filter(zayavka_id=obj.id)
    #     body = []
    #     for i in detali:
    #         body.append(self, i.ingridient, i.kolvo, i.ediz)
    #
    #     instance = super(Zayavka, self).save()
    #
    #     self.send_email()
    #
    #     return instance
    #
    # def send_email(self):
    #     msg = EmailMessage(
    #         'Кафе "У Дачи" отправило вам заявку на поставку продуктов',
    #         # body,
    #         'text',
    #         settings.EMAIL_HOST_USER,
    #         [self.postavshik.email],
    #     )
    #     msg.content_subtype = "html"
    #     msg.send()

    def save(self):
        detali = DetaliZayavki.objects.filter(zayavka_id=id(object))
        body = []

        for i in detali:
            ingridient = str(i.ingridient)
            # kolvo = str(i.kolvo)
            # ediz = str(i.ediz)
            body.append(ingridient)
        print(body)
        instance = super(Zayavka, self).save()
        self.send_email(body)
        return instance

    def send_email(self, body):


        msg = EmailMessage(
            'Кафе "У Дачи" отправило вам заявку на поставку продуктов',
             body,
             settings.EMAIL_HOST_USER,
             [self.postavshik.email],
        )

        msg.content_subtype = "html"
        msg.send()


class DetaliZayavki(models.Model):
    class Meta:
        verbose_name = 'Деталь Заявки'
        verbose_name_plural = 'Детали Заявки'

    zayavka = models.ForeignKey(Zayavka, verbose_name='Заявка', on_delete=models.SET_NULL, null=True, blank=False, related_name='detali_po_zaiavki')
    ingridient = models.ForeignKey(Ingridienti, verbose_name='Ингридиент', on_delete=models.SET_NULL, null=True,
                                   blank=False)
    kolvo = models.FloatField('Кол-во', default=1)
    ediz = models.IntegerField('Единица измерения', default=1, choices=(
        (1, 'шт'),
        (2, 'кг'),
        (3, 'л'),
    ))
    sklad = models.ForeignKey(Sklad, verbose_name='Склад', on_delete=models.SET_NULL, null=True, blank=False)
