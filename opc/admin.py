from django.conf.urls import url
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import *
from .ressources import *
from django.utils.html import format_html


# Register your models here.
#admin.site.register(RegOpcUaServer)
#admin.site.register(Dienstleistungen)
#admin.site.register(Produkt)
#admin.site.register(Kunden)
#admin.site.register(ProduktionsAuftrag)
#admin.site.register(Ressourcenplanung)
#admin.site.register(Serverdata)
#admin.site.register(Test)

# Header auf SmartParts AG setzen
admin.site.site_header = 'SmartsParts AG'

# Funktion um Virtuelle Server zu erzeugen und zu starten
def virt_serv_start(modeladmin, request, queryset):
    pass

    for object in queryset:
        name = object.servername
        port = object.portummer
        #handler = DockerHandler()
        #s_id = handler.create_server(name, port)
virt_serv_start.short_description = "Virtuelle Server anmelden"

# Funktion um Virtuelle Server abzumelden und herunter zu fahren
def virt_serv_stop(modeladmin, request, queryset):
    pass
    for object in queryset:
        name = object.servername
    #handler.remove_server(name)

virt_serv_stop.short_description = "Virtuelle Server stoppen"

# Demoprogramm auf Server laufen lassen
def demo_prog_start(modeladmin, request, queryset):
    pass
    for object in queryset:
        port = queryset.portnummer
        #ip = queryset.ip
        # string = ip+port
        #client = client(port)
        # client.startprogramm
virt_serv_stop.short_description = "Demoprogramm laufen lassen"


# Define the admin class
class RegOpcUaServerAdmin(ImportExportModelAdmin):
    list_display = ('regServerID', 'servername', 'portnummer', 'aktiv')
    list_filter = ('servername', 'portnummer')
    resource_class = RegOpcUaServerResource
    actions = [virt_serv_start, virt_serv_stop, demo_prog_start]
    list_per_page = 25
# Register the admin class with the associated model
admin.site.register(RegOpcUaServer, RegOpcUaServerAdmin)


# Register the Admin class for Dienstleistungen
class DienstleistungenAdmin(ImportExportModelAdmin):
    list_display = ('servicenummer', 'serviceName', 'serviceBeschreibung')
    list_filter = ('serviceName', 'servicenummer')
    list_per_page = 25
    resource_class = DienstleistungenResource
# Register the admin class with the associated model
admin.site.register(Dienstleistungen, DienstleistungenAdmin)


# Register the Admin class for Produkt
class ProduktAdmin(ImportExportModelAdmin):
    list_display = ('produktnummer', 'produktName', 'produktBeschreibung')
    list_filter = ('produktName', 'produktnummer')
    list_per_page = 25
    resource_class = ProduktResource
# Register the admin class with the associated model
admin.site.register(Produkt, ProduktAdmin)


# Register the Admin class for Kunden
class KundenAdmin(ImportExportModelAdmin):
    list_display = ('kundennummer', 'name', 'ort')
    list_filter = ('name', 'ort')
    list_per_page = 25
    resource_class = KundenResource
# Register the admin class with the associated model
admin.site.register(Kunden, KundenAdmin)


# Register the Admin class for ProduktionsAuftrag
class ProduktionsAuftragAdmin(ImportExportModelAdmin):
    list_display = ('auftragsnummer', 'kunde', 'produkt', 'server')
    list_filter = ('kunde', 'produkt')
    list_per_page = 25
    resource_class = ProduktionsAuftragResource
# Register the admin class with the associated model
admin.site.register(ProduktionsAuftrag, ProduktionsAuftragAdmin)


# Register the Admin class for Ressourcenplanung using
class RessourcenplanungAdmin(ImportExportModelAdmin):
    list_display = ('rplanungsnummer', 'planstatus', 'startdatum')
    list_filter = ('planstatus', 'startdatum')
    list_per_page = 25
    resource_class = RessourcenplanungResource
# Register the admin class with the associated model
admin.site.register(Ressourcenplanung, RessourcenplanungAdmin)


# Register the Admin class for Serverdata
class ServerdataAdmin(ImportExportModelAdmin):
    list_display = ('servername', 'start', 'beendet', 'stoerung')
    list_filter = ('servername', 'stoerung')
    list_per_page = 25
    resource_class = ServerdataResource
# Register the admin class with the associated model
admin.site.register(Serverdata, ServerdataAdmin)


# Register the Admin classes for Test using the decorator
@admin.register(Test)
class TestAdmin(ImportExportModelAdmin):
    pass
