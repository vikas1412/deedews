from django.contrib import admin
from homepage.models import Contact_User, Newsletter, IP_visitors


admin.site.register((Contact_User, Newsletter, IP_visitors))
