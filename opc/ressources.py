from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import *

# Ressouchenklassen für die Import und Exportfunktion von XML, json , CSV , yaml

class RegOpcUaServerResource(resources.ModelResource):
    class Meta:
        model = RegOpcUaServer


class DienstleistungenResource(resources.ModelResource):
    class Meta:
        model = Dienstleistungen


class ProduktResource(resources.ModelResource):
    class Meta:
        model = Produkt


class KundenResource(resources.ModelResource):
    class Meta:
        model = Kunden


class ProduktionsAuftragResource(resources.ModelResource):
    class Meta:
        model = ProduktionsAuftrag


class RessourcenplanungResource(resources.ModelResource):
    class Meta:
        model = Ressourcenplanung


class ServerdataResource(resources.ModelResource):
    class Meta:
        model = Serverdata
