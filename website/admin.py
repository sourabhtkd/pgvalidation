import csv

from django.contrib.admin import register
from django.http import HttpResponse

from website import models
from django.contrib import admin

from website.forms import MembershipForm

admin.autodiscover()
admin.site.enable_nav_sidebar = False


@register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'actual_price', 'duration_type', 'duration', 'created_on',
                    'is_active']

    form = MembershipForm
    readonly_fields = ['created_on']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export CSV"


@register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@register(models.UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    pass
