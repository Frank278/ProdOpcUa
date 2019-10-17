from django.contrib.auth.models import User, Group
from rest_framework import serializers

import opc, objects
from .models import *
from rest_framework import serializers



class ProduktionsAuftragSerializer(serializers.Serializer):
    # eindeutige Kundennumnmer
    auftragsnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    # Kunde des Auftrages
    kunde = models.ForeignKey(to=Kunden, on_delete=models.SET_NULL, null=True)
    # Produkt des Auftrages
    produkt = models.ForeignKey(to=Produkt, on_delete=models.SET_NULL, null=True)
    # Aktueller Schritt
    aktuellerSchritt = models.PositiveIntegerField(null=True)
    # Zugeteilter Server zum Auftrag
    server = models.ForeignKey(to=RegOpcUaServer, on_delete=models.SET_NULL, null=True)
    # Anzahl der Schritte
    anzahlSchritte = models.PositiveIntegerField(null=True)
    # Auftragsstaus
    AUFTRAGSSTATUS = Choices('Geplant', 'InBearbeitung', 'Gestoppt', 'Abgeschossen')
    auftragsstatus = models.CharField(choices=AUFTRAGSSTATUS, default=AUFTRAGSSTATUS.Geplant,
                                      max_length=20)
    # letzte Aktuallisierung
    letzteAktuallisierung = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return opc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.kunde = validated_data.get('kunde', instance.kunde)
        instance.produkt = validated_data.get('produkt', instance.produkt)
        instance.aktuellerSchritt = validated_data.get('aktuellerSchritt', instance.aktuellerSchritt)
        instance.server = validated_data.get('server', instance.server)
        instance.anzahlSchritte = validated_data.get('anzahlschritte', instance.anzahlSchritte)
        instance.auftragsstatus = validated_data.get('auftragsstaus', instance.auftragsstatus)
        instance.letzteAktuallisierung = validated_data.get('letzteAktualisierung', instance.letzteAktuallisierung)

        instance.save()
        return instance





