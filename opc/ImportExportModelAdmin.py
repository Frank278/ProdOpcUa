from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import ProduktionsAuftrag


@admin.register(ProduktionsAuftrag)
class ProduktionsAuftragAdmin(ImportExportModelAdmin):
    pass

