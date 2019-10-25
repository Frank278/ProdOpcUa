from django.contrib.auth.models import User, Group
from rest_framework import serializers

import opc, objects
from .models import *
from rest_framework import serializers

# Hier wird desn REST Service serialisiert

class RegOpcUaServerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RegOpcUaServer
        fields = ['regServerID', 'servername', 'portnummer']


class DienstleistungenSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Dienstleistungen
        fields = ['servicenummer', 'serviceName', 'serviceBeschreibung']


class KundenSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Kunden
        fields = ['kundennummer', 'name', 'ort']

class ProduktSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Produkt
        fields = ['produktnummer', 'produktName', 'produktBeschreibung']

class ProduktionsAuftragSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProduktionsAuftrag
        fields = ['auftragsnummer', 'anzahlSchritte', 'auftragsstatus']

class RessourcenplanungSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ressourcenplanung
        fields = ['rplanungsnummer', 'planstatus', 'startdatum']
