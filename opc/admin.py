from django.conf.urls import url
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import *
from .ressources import *
from django.utils.html import format_html
from ServerAndClient.controller import controller
from ServerAndClient.client import client


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
#######################################################################################################################
# Hier stehen die Methoden und Funktionen
#######################################################################################################################

# Instanz vom Dockerhandler erstellen
_docker_handler = None
def get_docker_handler():
    global _docker_handler
    if not _docker_handler:
        _docker_handler = controller.DockerHandler()
    return _docker_handler

# Hier wird der virtuell Server im Docker erzeugt


def virt_serv_start(modeladmin, request, queryset):
    for object in queryset:
        name = object.servername
        port = object.portnummer
        handler = get_docker_handler()
        s_id = handler.create_server(name, port)
        queryset.update(aktiv=True)
        queryset.update(serverstatus='Gestartet')
        queryset.update(servertyp='Virtuell')
virt_serv_start.short_description = "Virtuellen Server anmelden"

# Funktion um Virtuelle Server abzumelden und herunter zu fahren
def virt_serv_stop(modeladmin, request, queryset):
    for object in queryset:
        name = object.servername
        queryset.update(aktiv=False)
        queryset.update(serverstatus='Gestoppt')
        handler = get_docker_handler()
        handler.remove_server(name)


virt_serv_stop.short_description = "Virtuelle Server stoppen"

# erstellt einen Client Docker , wenn der Server nicht virtuell ist.
# also ein Raspery oder eine reale Maschine
def virt_client_create(modeladmin, request, queryset):
    # for object in queryset:
    #     if object.servertyp == 'Raspery':
    #         name = object.servername
    #         port = object.portnummer
    #         handler = get_docker_handler()
    #         s_id = handler.create_client(name, port)
    pass # konnte nicht mehr getestet werden
virt_client_create.short_description = "Client erstellen für Raspery"

# Demoprogramm auf nicht vituellen Server laufen lassen
def ua_prog_start(modeladmin, request, queryset):
    # for object in queryset:
    #     if object.servertyp == 'Raspery':
    #         name = object.servername
    #         port = queryset.uamethod
    #         serverurl = object.ip
    #         uamethod = object.uamethod
    #         handler = get_docker_handler()
    #         s_id = handler.create_client(name, serverurl, port, uamethod)
    pass # konnte nicht mehr getestet werden

ua_prog_start.short_description = "UA-Mehtode aufrufen auf Raspery Server"

# Demoprogramm auf Server laufen lassen
def virt_serv_signal(modeladmin, request, queryset):
    for object in queryset:
        name = object.servername
    if object.maschinenstatus=='Bereit':
        queryset.update(maschinenstatus='Maschine belegt')
    elif object.maschinenstatus=='Maschine belegt':
        queryset.update(maschinenstatus='Bereit')

    handler = get_docker_handler()
    handler.signal_server(name)
virt_serv_signal.short_description = "Maschinen Status ändern"

#######################################################################################################################
# Ab Hier beginen die Admin-Klassen
#
#######################################################################################################################

# Define the admin class
class RegOpcUaServerAdmin(ImportExportModelAdmin):
    list_display = ('regServerID', 'servername', 'portnummer', 'aktiv', 'serverstatus','maschinenstatus')
    list_filter = ('servername', 'portnummer')
    resource_class = RegOpcUaServerResource
    actions = [virt_serv_start, virt_serv_stop, virt_serv_signal, virt_client_create, ua_prog_start]
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
    list_display = ('auftragsnummer', 'kunde', 'produkt')
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
    list_display = ('servername', 'status', 'temp', 'press', 'time')
    list_filter = ('servername', 'status')
    list_per_page = 25
    resource_class = ServerdataResource
# Register the admin class with the associated model
admin.site.register(Serverdata, ServerdataAdmin)


