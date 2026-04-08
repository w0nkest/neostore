from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Certificate)
admin.site.register(Thing)
admin.site.register(Order)

# @admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
