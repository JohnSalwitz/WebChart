
from django.contrib import admin
from .models import DAU

class DAUAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date',               {'fields': ['date']}),
        ('Active Users',       {'fields': ['active_users']}),
    ]

admin.site.register(DAU, DAUAdmin)

