from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CustomAdminSite(admin.AdminSite):
    site_header = _("True.org.il admin")
    site_title = _("True.org.il admin")


admin_site = CustomAdminSite(name="custom_admin")
