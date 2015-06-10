from django.contrib import messages
from django import http
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from oscar.apps.checkout.views import PaymentDetailsView
from oscar.core.loading import get_class, get_classes, get_model
from oscar.apps.payment.models import SourceType, Source
from cashondelivery.forms import BillingAddressForm
from cashondelivery import gateway


BillingAddress = get_model("order", "BillingAddress")

class PaymentDetailsView(PaymentDetailsView):
    template_name = 'cashondelivery/payment_details.html'
    template_name_preview = 'cashondelivery/preview.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        if 'billing_address_form' not in kwargs:
            ctx['billing_address_form'] = self.get_billing_address_form(
                ctx['shipping_address']
            )
        elif kwargs['billing_address_form'].is_valid():
            # On the preview view, we extract the billing address into the
            # template context so we can show it to the customer.
            ctx['billing_address'] = kwargs[
                'billing_address_form'].save(commit=False)
        return ctx

    def get_billing_address_form(self, billing_address):
        """
        Return an instantiated billing address form
        """
        addr = self.get_default_billing_address()
        if not addr:
            return BillingAddressForm(billing_address)
        billing_addr = BillingAddress()
        addr.populate_alternative_model(billing_addr)
        return BillingAddressForm(billing_address,
                                  instance=billing_addr)

    def handle_payment_details_submission(self, request):
        # Validate the submitted forms
        shipping_address = self.get_shipping_address(
            self.request.basket)
        address_form = BillingAddressForm(shipping_address, request.POST)

        if address_form.is_valid():
            if address_form.cleaned_data["same_as_shipping"] == "same":
                self.checkout_session.bill_to_shipping_address()
            if address_form.cleaned_data["same_as_shipping"] == "new":
                address_fields = dict(
                    (k, v) for (k, v) in address_form.instance.__dict__.items()
                    if not k.startswith('_') and not k.startswith('same_as_shipping')) 
                self.checkout_session.bill_to_new_address(address_fields)
            return self.render_preview(
                request, billing_address_form=address_form)

        # Forms are invalid - show them to the customer along with the
        # validation errors.
        return self.render_payment_details(
            request, billing_address_form=address_form)

    def handle_payment(self, order_number, total, **kwargs):
        reference = gateway.create_transaction(order_number,total)
        source_type, is_created = SourceType.objects.get_or_create(
            name='Cash on Delivery')
        source = Source(source_type=source_type,
                        currency=total.currency,
                        amount_allocated=total.incl_tax,
                        amount_debited=total.incl_tax)
        self.add_payment_source(source)
        self.add_payment_event('Issued', total.incl_tax,
                               reference=reference)
