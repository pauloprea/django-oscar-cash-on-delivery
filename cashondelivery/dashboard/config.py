from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DashboardConfig(AppConfig):
    label = 'cashondelivery_dashboard'
    name = 'cashondelivery.dashboard'
    verbose_name = _('Cash On Delivery dashboard')
