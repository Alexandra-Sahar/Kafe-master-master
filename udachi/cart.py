from decimal import Decimal
from django.conf import settings
from udachi.models import Bluda


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, Bluda, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        bluda_id = str(Bluda.id)

        if bluda_id not in self.cart:
            self.cart[bluda_id] = {'quantity': 0,
                                   'price': str(Bluda.cena),
                                   'название' : str(Bluda.nazvanie),
                                   'prevyu' : str(Bluda.prevyu),
                                   'top' : Bluda.kolvo_dobavlenia_v_korzinu}
        if update_quantity:
            self.cart[bluda_id]['quantity'] = quantity
            self.cart[bluda_id]['top'] += 1
        else:
            self.cart[bluda_id]['quantity'] += quantity
            self.cart[bluda_id]['top'] += 1
        self.cart[bluda_id]['top'] += 1
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, bluda):
        """
        Удаление товара из корзины.
        """
        bluda_id = str(bluda.id)
        if bluda_id in self.cart:
            del self.cart[bluda_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        bluda_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        bludas = Bluda.objects.filter(id__in=bluda_ids)
        for bluda in bludas:
            self.cart[str(bluda.id)]['bluda'] = bluda

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
