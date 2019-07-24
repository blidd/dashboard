from django.contrib import admin

from .models import Headline, CustomUser


admin.site.register(Headline)
admin.site.register(CustomUser)
