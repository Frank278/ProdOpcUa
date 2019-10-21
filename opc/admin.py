from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import *
from .ressources import *


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
class RegOpcUaServerAdmin(ImportExportModelAdmin):
    list_display = ('regServerID', 'servername', 'portnummer', 'aktiv')
    list_filter = ('servername', 'portnummer')
    resource_class = RegOpcUaServerResource
# Register the admin class with the associated model
admin.site.register(RegOpcUaServer, RegOpcUaServerAdmin)


# Register the Admin class for Dienstleistungen
class DienstleistungenAdmin(ImportExportModelAdmin):
    list_display = ('servicenummer', 'serviceName', 'serviceBeschreibung')
    list_filter = ('serviceName', 'servicenummer')
    resource_class = DienstleistungenResource
# Register the admin class with the associated model
admin.site.register(Dienstleistungen, DienstleistungenAdmin)


# Register the Admin class for Produkt
class ProduktAdmin(ImportExportModelAdmin):
    list_display = ('produktnummer', 'produktName', 'produktBeschreibung')
    list_filter = ('produktName', 'produktnummer')
    resource_class = ProduktResource
admin.site.register(Produkt, ProduktAdmin)


# Register the Admin class for Kunden
class KundenAdmin(ImportExportModelAdmin):
    list_display = ('kundennummer', 'name', 'ort')
    list_filter = ('name', 'ort')
    resource_class = KundenResource
admin.site.register(Kunden, KundenAdmin)


# Register the Admin class for ProduktionsAuftrag
class ProduktionsAuftragAdmin(ImportExportModelAdmin):
    list_display = ('auftragsnummer', 'kunde', 'produkt', 'server')
    list_filter = ('kunde', 'produkt')
    resource_class = ProduktionsAuftragResource
admin.site.register(ProduktionsAuftrag, ProduktionsAuftragAdmin)


# Register the Admin class for Ressourcenplanung using
class RessourcenplanungAdmin(ImportExportModelAdmin):
    list_display = ('rplanungsnummer', 'planstatus', 'startdatum')
    list_filter = ('planstatus', 'startdatum')
    resource_class = RessourcenplanungResource
admin.site.register(Ressourcenplanung, RessourcenplanungAdmin)


# Register the Admin class for Serverdata
class ServerdataAdmin(ImportExportModelAdmin):
    list_display = ('servername', 'start', 'beendet', 'stoerung')
    list_filter = ('servername', 'stoerung')
    resource_class = ServerdataResource
admin.site.register(Serverdata, ServerdataAdmin)


# Register the Admin classes for Test using the decorator
@admin.register(Test)
class TestAdmin(ImportExportModelAdmin):
    pass
