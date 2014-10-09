from django.views.generic import ListView, DetailView

from cashondelivery import models


class TransactionListView(ListView):
    model = models.CashOnDeliveryTransaction
    context_object_name = 'transactions'
    template_name = 'dashboard/cashondelivery/transaction_list.html'


class TransactionDetailView(DetailView):
    model = models.CashOnDeliveryTransaction
    context_object_name = 'txn'
    template_name = 'dashboard/cashondelivery/transaction_detail.html'

