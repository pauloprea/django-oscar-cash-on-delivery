from django import forms

from oscar.apps.payment import forms as payment_forms
from oscar.core.loading import get_class, get_classes, get_model


Country = get_model('address', 'Country')
BillingAddress = get_model("order", "BillingAddress")

class BillingAddressForm(payment_forms.BillingAddressForm):
    """
    Extended version of the core billing address form that adds a field so
    customers can choose to re-use their shipping address.
    """
    SAME_AS_SHIPPING, NEW_ADDRESS = 'same', 'new'
    CHOICES = (
        (SAME_AS_SHIPPING, 'Same as the shipping address'),
        (NEW_ADDRESS, 'Enter a new address'),
    )
    same_as_shipping = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CHOICES, initial=SAME_AS_SHIPPING)

    class Meta(payment_forms.BillingAddressForm):
        model = BillingAddress
        exclude = ('search_text', 'first_name', 'last_name')

    def __init__(self, shipping_address, data=None, *args, **kwargs):
        # Store a reference to the shipping address
        self.shipping_address = shipping_address

        super(BillingAddressForm, self).__init__(data, *args, **kwargs)
        self.adjust_country_field()

        # If no shipping address (eg a download), then force the
        # 'same_as_shipping' field to have a certain value.
        if shipping_address is None:
            self.fields['same_as_shipping'].choices = (
                (self.NEW_ADDRESS, 'Enter a new address'),)
            self.fields['same_as_shipping'].initial = self.NEW_ADDRESS

        # If using same address as shipping, we don't need require any of the
        # required billing address fields.
        if data and data.get('same_as_shipping', None) == self.SAME_AS_SHIPPING:
            for field in self.fields:
                if field != 'same_as_shipping':
                    self.fields[field].required = False

    def _post_clean(self):
        # Don't run model validation if using shipping address
        if self.cleaned_data.get('same_as_shipping') == self.SAME_AS_SHIPPING:
            return
        super(BillingAddressForm, self)._post_clean()

    def save(self, commit=True):
        if self.cleaned_data.get('same_as_shipping') == self.SAME_AS_SHIPPING:
            # Convert shipping address into billing address
            billing_addr = BillingAddress()
            self.shipping_address.populate_alternative_model(billing_addr)
            if commit:
                billing_addr.save()
            return billing_addr
        instance = super(BillingAddressForm, self).save(commit=False)
        instance.state = self.cleaned_data["stateorcounty"].name
        if commit:
            instance.save()
        return instance

    def adjust_country_field(self):
        countries = Country._default_manager.filter(
            is_shipping_country=True)

        # No need to show country dropdown if there is only one option
        if len(countries) == 1:
            del self.fields['country']
            self.instance.country = countries[0]
        else:
            self.fields['country'].queryset = countries
            self.fields['country'].empty_label = None