from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(RegOpcUaServer)
#admin.site.register(Dienstleistungen)
#admin.site.register(Produkt)
#admin.site.register(Kunden)
#admin.site.register(ProduktionsAuftrag)
#admin.site.register(Ressourcenplanung)
#admin.site.register(Serverdata)
#admin.site.register(Test)


# Define the admin class
class RegOpcUaServerAdmin(admin.ModelAdmin):
    list_display = ('regServerID', 'servername', 'portnummer', 'aktiv')

# Register the admin class with the associated model
admin.site.register(RegOpcUaServer, RegOpcUaServerAdmin)

# Register the Admin classes for Dienstleistungen using the decorator
@admin.register(Dienstleistungen)
class DienstleistungenAdmin(admin.ModelAdmin):
    list_display = ('servicenummer', 'serviceName', 'serviceBeschreibung')

# Register the Admin classes for Produkt using the decorator
@admin.register(Produkt)
class ProduktAdmin(admin.ModelAdmin):
    list_display = ('produktnummer', 'produktName', 'produktBeschreibung')


# Register the Admin classes for Kunden using the decorator
@admin.register(Kunden)
class KundenAdmin(admin.ModelAdmin):
    list_display = ('kundennummer','name', 'ort')
    list_filter = ('name', 'ort')

class ProduktionsAuftragResource(resources.ModelResource):
    class Meta:
        model = ProduktionsAuftrag


# Register the Admin class for ProduktionsAuftrag
#@admin.register(ProduktionsAuftrag)
class ProduktionsAuftragAdmin(ImportExportModelAdmin):
    list_display = ('auftragsnummer', 'kunde', 'produkt', 'server')
    resource_class = ProduktionsAuftragResource
admin.site.register(ProduktionsAuftrag, ProduktionsAuftragAdmin)

class RessourcenplanungResource(resources.ModelResource):
    class Meta:
        model = Ressourcenplanung

# Register the Admin classes for Ressourcenplanung using
class RessourcenplanungAdmin(ImportExportModelAdmin):
    list_display = ('rplanungsnummer', 'planstatus', 'startdatum')
    resource_class = RessourcenplanungResource
admin.site.register(Ressourcenplanung, RessourcenplanungAdmin)


# Register the Admin classes for Serverdata using the decorator
@admin.register(Serverdata)
class ServerdataAdmin(admin.ModelAdmin):
    list_display = ('servername', 'start', 'beendet', 'stoerung')


# Register the Admin classes for Test using the decorator
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass
