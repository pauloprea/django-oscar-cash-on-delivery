from django.contrib import admin
from cashondelivery.models import CashOnDeliveryTransaction


class CashOnDeliveryTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'method', 'amount', 'reference',
                       'confirmed', 'date_confirmed', 'date_created')


admin.site.register(CashOnDeliveryTransaction, CashOnDeliveryTransactionAdmin)