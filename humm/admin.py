from django.contrib import admin
from .models import Humm
# Register your models here


class HummAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')
    search_fields = ['user__username', 'user__email']

    class Meta:
        model = Humm


admin.site.register(Humm, HummAdmin)
