from django.contrib import admin
from house.models import House


class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('ev_fiyati',)


admin.site.register(House, HouseAdmin)