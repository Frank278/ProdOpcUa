from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from model_utils import Choices
from datetime import datetime
from django.utils import timezone
from datetime import timedelta


class VirtuelleOpcUaServer(models.Model):
    # eindeutige ID für Vitruellen Servers
    virtuellServerID = models.PositiveSmallIntegerField(default=0, unique=True)
    # Name des Servers
    servername = models.CharField(max_length=30, unique=True)
    ort = models.CharField(max_length=30)
    portnummer = models.PositiveIntegerField(null=True)
    SERVERSTATUS = Choices('Starten', 'Gestartet', 'Stoppen', 'Gestoppt')
    serverstatus = models.CharField(choices=SERVERSTATUS, default=SERVERSTATUS.Gestoppt, max_length=20)
    autoStart = models.BooleanField(default=False)
    anzahlOffeneAuftraege = models.PositiveIntegerField(null=True)
    anzahlAbgesAuftraege = models.PositiveIntegerField(null=True)
    aktuelleAuftraegsNr = models.PositiveIntegerField(null=True)
    startZeit = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.servername


class DienstVirtOpcUaServer(models.Model):
    # eindeutige ID für Dienstleistungen des virtuellen Servers
    dieVirtOpcUaID = models.PositiveSmallIntegerField(default=0, unique=True)
    virtserver = models.ForeignKey(to=VirtuelleOpcUaServer, on_delete=models.SET_NULL, null=True)
    running_simulation = models.DurationField(default=timedelta(minutes=2))
    serviceBeschreibung = models.TextField(max_length=200, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.dieVirtOpcUaID


class RegOpcUaServer(models.Model):
    # eindeutige ID für Vitruellen Servers
    regServerID = models.PositiveSmallIntegerField(default=0, unique=True)
    # Name des Servers
    servername = models.CharField(max_length=30, unique=True)
    ort = models.CharField(max_length=30)
    portnummer = models.PositiveIntegerField(null=True)
    REGISTRIERUNGSSTATUS = Choices('Starten', 'Gestartet', 'Stoppen', 'Gestoppt')
    registrieungsstatus = models.CharField(choices=REGISTRIERUNGSSTATUS, default=REGISTRIERUNGSSTATUS.Gestoppt,
                                           max_length=20)

    regestrierungsZeit = models.DateTimeField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.servername


class DienstOpcUaServer(models.Model):
    # eindeutige ID für Dienstleistungen des virtuellen Servers
    dieOpcUaID = models.PositiveSmallIntegerField(default=0, unique=True)
    regServer = models.ForeignKey(to=RegOpcUaServer, on_delete=models.SET_NULL, null=True)
    serviceBeschreibung = models.TextField(max_length=200, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.dieOpcUaID


class Dienstleistungen(models.Model):
    # eindeutige ID für Dienstleistungen aller Server
    servicenummer = models.PositiveSmallIntegerField(default=0, unique=True)
    dieOpcUa = models.ManyToManyField('DienstOpcUaServer')
    dieVirtOpcUa = models.ManyToManyField('DienstVirtOpcUaServer')
    serviceName = models.CharField(max_length=30, unique=True)
    serviceBeschreibung = models.TextField(max_length=200, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.serviceName


class DieIntProdukt(models.Model):
    # eindeutige ID für Dienstleistung für intelligentes Produkt
    dieIntProduktID = models.PositiveSmallIntegerField(default=0, unique=True)
    servicenummer = models.ManyToManyField('Dienstleistungen')
    anzahlService = models.PositiveIntegerField(null=True)
    sequenz = models.PositiveIntegerField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.dieIntProduktID


class IntProdukt(models.Model):
    # eindeutige ID für intelligentes Produkt
    intProduknummer = models.PositiveSmallIntegerField(default=0, unique=True)
    dieIntProd = models.ForeignKey(to=Dienstleistungen, on_delete=models.SET_NULL, null=True)
    produktName = models.CharField(max_length=30)
    produktBeschreibung = models.TextField(max_length=200, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.produktName


class Kunden(models.Model):
    # eindeutige Kundennumnmer

    kundennummer = models.PositiveSmallIntegerField(default=0, unique=True)
    name = models.CharField(max_length=30)
    Telefonnummer = models.PositiveIntegerField(null=True)

    ort = models.CharField(max_length=30)
    plz = models.PositiveIntegerField(null=True)
    strasse = models.CharField(max_length=30)
    hausnummer = models.PositiveIntegerField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class ProduktionsAuftrag(models.Model):
    # eindeutige Kundennumnmer
    auftragsnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    kundennummer = models.ForeignKey(to=Kunden, on_delete=models.SET_NULL, null=True)
    intProdukt = models.ForeignKey(to=IntProdukt, on_delete=models.SET_NULL, null=True)
    aktuellerSchritt = models.PositiveIntegerField(null=True)
    anzahlschritte = models.PositiveIntegerField(null=True)
    fortschritt = models.PositiveIntegerField(null=True)
    AUFTRAGSSTATUS = Choices('Geplant', 'InBearbeitung', 'Gestoppt', 'Abgeschossen')
    auftragsstatus = models.CharField(choices=AUFTRAGSSTATUS, default=AUFTRAGSSTATUS.Geplant,
                                      max_length=20)
    letzteAktuallisierung = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.auftragsnummer


class Ressourcenplanung(models.Model):
    # eindeutige ID für die Ressouchenplannung
    rplanungsnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    produktionsuauftrag = models.ForeignKey(to= ProduktionsAuftrag, on_delete=models.SET_NULL, null=True)
    dienstleistungen = models.ManyToManyField('Dienstleistungen')
    PLANSTATUS = Choices('Geplant', 'InBearbeitung', 'Laufend', 'Abgeschossen')
    planstatus = models.CharField(choices=PLANSTATUS, default=PLANSTATUS.Geplant, max_length=20)
    startdatum = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)
    enddatum = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.rplanungsnummer
