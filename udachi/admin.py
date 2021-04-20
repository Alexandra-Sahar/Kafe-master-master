from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin

from udachi.models import TipBluda, Bluda, Ingridienti, IngridientiVBlude, Akzia, Zakaz, Otzivi


class TipBludaAdmin(ImportExportModelAdmin):
    pass


admin.site.register(TipBluda, TipBludaAdmin)


class IngridientiAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Ingridienti, IngridientiAdmin)


class IngridientiVBludeInline(admin.TabularInline):
    model = IngridientiVBlude


class BludaAdmin(ImportExportModelAdmin):
    inlines = [
        IngridientiVBludeInline,
    ]
    list_display = [
        'id',
        'nazvanie',
        'opisanie',
        'cena',
        'gramovka',
        'tip_bluda',
        'ne_pokazivat',
        'kolvo_dobavlenia_v_korzinu'
    ]
    list_filter = ('tip_bluda', 'ne_pokazivat')
    readonly_fields = ['kolvo_dobavlenia_v_korzinu', ]
    list_display_links = ['nazvanie', ]
    search_fields = ['nazvanie', 'cena', 'tip_bluda__nazvanie']
    list_editable = ['opisanie', 'cena', 'gramovka', 'tip_bluda', 'ne_pokazivat']
    ordering = ['-nazvanie', ]


admin.site.register(Bluda, BludaAdmin)


class AkziaAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'nazvanie',
    ]
    # list_filter = ('nazvanie',)
    list_display_links = ['id', ]
    search_fields = ['nazvanie', ]
    list_editable = ['nazvanie', ]
    ordering = ['-nazvanie', ]


admin.site.register(Akzia, AkziaAdmin)


class ZakazAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'sposob_otdachi',
        'telephone',
        'fio',
        'akzia',
        'data_i_vremia_zakaza',
        'adres',
        'stolik',
        'zakaz_proveden'
    ]

    list_filter = ('sposob_otdachi', 'akzia', 'stolik', 'zakaz_proveden')
    list_display_links = ['id', ]
    search_fields = ['telephone', 'data_i_vremia_zakaza', 'fio', 'adres', 'stolik']
    # list_editable = [ 'nazvanie', ]

    ordering = ['data_i_vremia_zakaza', ]


admin.site.register(Zakaz, ZakazAdmin)


class OtziviAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'avtor',
        'get_short_opisanie',
        'telephone_avtora',
        'data_otziva',
        'prosli_moderaziu',

    ]

    list_filter = ('data_otziva', 'prosli_moderaziu')
    list_display_links = ['id', ]
    search_fields = ['avtor', 'otziv', 'telephone_avtora', 'data_otziva']
    list_editable = ['prosli_moderaziu', ]

    ordering = ['data_otziva', ]


admin.site.register(Otzivi, OtziviAdmin)
