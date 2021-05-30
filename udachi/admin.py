from django.contrib import admin


from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin

from udachi.models import TipBluda, Bluda, Ingridienti, IngridientiVBlude, Zakaz, Otzivi, DetaliZakaza, Zayavka, \
    DetaliZayavki, Postavshiki, Sklad, Bronirovanie


class TipBludaAdmin(ImportExportModelAdmin):
    pass


admin.site.register(TipBluda, TipBludaAdmin)


class IngridientiAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Ingridienti, IngridientiAdmin)


class IngridientiVBludeInline(admin.TabularInline):
    model = IngridientiVBlude


class DetaliZakazaInline(admin.TabularInline):
    model = DetaliZakaza


class DetaliZayavkiInline(admin.TabularInline):
    model = DetaliZayavki


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




class BronirovanieAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'data',
        'telephone',
        'fio',
        'stolik',
    ]

    list_display_links = ['id', ]
    search_fields = ['data', 'telephone', 'fio', 'stolik', ]
    list_editable = ['data', ]
    ordering = ['data', ]

admin.site.register(Bronirovanie, BronirovanieAdmin)


class ZakazAdmin(ImportExportModelAdmin):
    inlines = [
        DetaliZakazaInline,
    ]
    list_display = [
        'id',
        'sposob_otdachi',
        'telephone',
        'fio',
        'data_i_vremia_zakaza',
        'adres',
        'zakaz_proveden'
    ]

    list_filter = ('sposob_otdachi',   'zakaz_proveden')
    list_display_links = ['id', ]
    search_fields = ['telephone', 'data_i_vremia_zakaza', 'fio', 'adres' ]
    # list_editable = [ 'nazvanie', ]

    ordering = ['data_i_vremia_zakaza', ]


admin.site.register(Zakaz, ZakazAdmin)


class ZayavkaAdmin(ImportExportModelAdmin):
    inlines = [
        DetaliZayavkiInline,
    ]
    list_display = [
        'id',
        'postavshik',
        'data',
        'status',
        'ispolnitel',
    ]

    list_filter = ('postavshik', 'data', 'status', 'ispolnitel')
    list_display_links = ['id', ]
    search_fields = ['postavshik', 'data', 'status', 'ispolnitel']

    ordering = ['data', ]


admin.site.register(Zayavka, ZayavkaAdmin)


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


class PostavshikiAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'naimenovanie',
        'telephone',
        'email',
        'adres',
        'opisanie',
        'inn',
    ]

    list_display_links = ['id', ]
    search_fields = ['naimenovanie', 'telephone', 'inn']


admin.site.register(Postavshiki, PostavshikiAdmin)


class SkladAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'nazvanie',
    ]

    search_fields = ['nazvanie']


admin.site.register(Sklad, SkladAdmin)
