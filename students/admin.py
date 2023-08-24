from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from import_export import resources
from .models import Claim
# Register your models here.
class ClaimResource(resources.ModelResource):
    class Meta:
        model = Claim


class ClaimAdmin(ImportExportModelAdmin):
    resource_classes = [ClaimResource]


admin.site.register(Claim, ClaimAdmin)
