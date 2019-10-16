from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from model_utils import Choices
from datetime import datetime
from django.utils import timezone
from datetime import timedelta



class RegOpcUaServer(models.Model):
    # eindeutige ID für den Servers
    regServerID = models.PositiveSmallIntegerField(default=0, unique=True)
    # Name des Servers
    servername = models.CharField(max_length=30, unique=True)
    # Ort des Servers
    ort = models.CharField(max_length=30)
    # Port des Servers
    portnummer = models.PositiveIntegerField(null=True)

    # Art des Servers
    SERVERTYP = Choices('Raspery', 'Virtuell')
    servertyp = models.CharField(choices=SERVERTYP, default=SERVERTYP.Raspery,
                                           max_length=20)
    # Zeit der Anmeldung beim Server
    regestrierungsZeit = models.DateTimeField(null=True)

    # Status des virtuellen Servers
    SERVERSTATUS = Choices('Starten', 'Gestartet', 'Stoppen', 'Gestoppt')
    serverstatus = models.CharField(choices=SERVERSTATUS, default=SERVERSTATUS.Gestoppt, max_length=20)

    # Automatischer Start bei starten der Applikation
    autoStart = models.BooleanField(default=False)


    def __str__(self):
        """String for representing the Model object."""
        return self.servername





class Dienstleistungen(models.Model):
    # eindeutige ID für Dienstleistungen aller Server
    servicenummer = models.PositiveSmallIntegerField(default=0, unique=True)
    # eingebunde Server für die Dienstleistungen
    dieOpcUa = models.ManyToManyField('RegOpcUaServer', blank=True)

    # Name des Service
    serviceName = models.CharField(max_length=30, unique=True)
    # Beschreibung des Service
    serviceBeschreibung = models.TextField(max_length=200, blank=True, null=True)

    # Simmulierte Zeit
    running_simulation = models.DurationField(default=timedelta(minutes=2))


    def __str__(self):
        """String for representing the Model object."""
        return self.serviceName





class Produkt(models.Model):
    # eindeutige ID für intelligentes Produkt
    produktnummer = models.PositiveSmallIntegerField(default=0, unique=True)

    # Produktname
    produktName = models.CharField(max_length=30)

    # Produktbeschreibung
    produktBeschreibung = models.TextField(max_length=200, null=True)

    # Servivenummern der Dienstleistungen
    servicenummern = models.ManyToManyField('Dienstleistungen')

    # Anzahl der benötigten Service
    anzahlService = models.PositiveIntegerField(null=True)


    # Berechnung der erstellungszeit des Produktes
    @property
    def erstellungszeit(self):
        anzahl = self.anzahlService
        zeitproservice = timedelta(minutes=10)
        ezeit = anzahl*zeitproservice

        return ezeit


    def __str__(self):
        """String for representing the Model object."""
        return self.produktName


class Kunden(models.Model):
    # eindeutige Kundennumnmer
    kundennummer = models.PositiveSmallIntegerField(default=0, unique=True)
    # Name des Kunden
    name = models.CharField(max_length=30, null=True)
    # Telefonnummer des Kunden
    telefonnummer = models.PositiveIntegerField(null=True)
    # Ort des Kunden
    ort = models.CharField(max_length=30)
    # PLZ des Kunden
    plz = models.PositiveIntegerField(null=True)
    # Strasse de Kunden
    strasse = models.CharField(max_length=30)
    # Hausnummer des Kunden
    hausnummer = models.PositiveIntegerField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class ProduktionsAuftrag(models.Model):
    # eindeutige Kundennumnmer
    auftragsnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    # Kundenmummer des Auftrages
    kundennummer = models.ForeignKey(to=Kunden, on_delete=models.SET_NULL, null=True)
    intProdukt = models.ForeignKey(to=Produkt, on_delete=models.SET_NULL, null=True)
    aktuellerSchritt = models.PositiveIntegerField(null=True)
    anzahlSchritte = models.PositiveIntegerField(null=True)
    AUFTRAGSSTATUS = Choices('Geplant', 'InBearbeitung', 'Gestoppt', 'Abgeschossen')
    auftragsstatus = models.CharField(choices=AUFTRAGSSTATUS, default=AUFTRAGSSTATUS.Geplant,
                                      max_length=20)
    letzteAktuallisierung = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)

    # berechnung des fortschrittes des Auftrages
    @property
    def fortschritt(self):


        aktuellerSchritt = self.aktuellerSchritt
        anzahlSchritte =self.anzahlSchritte
        fortschritt= (aktuellerSchritt*100)/anzahlSchritte

        return int(fortschritt)



  #  for i in range(n)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.auftragsnummer)


class Ressourcenplanung(models.Model):
    # eindeutige ID für die Ressouchenplannung
    rplanungsnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    # Produktionsaufträge für den Ressourcenplan
    produktionsauftrag = models.ManyToManyField('ProduktionsAuftrag')
    # Dienstleistungsplan für den Ressourcenplan
    dienstleistungen = models.ManyToManyField('Dienstleistungen')
    # Status des Ressouchenplanes
    PLANSTATUS = Choices('Geplant', 'InBearbeitung', 'Laufend', 'Abgeschossen')
    planstatus = models.CharField(choices=PLANSTATUS, default=PLANSTATUS.Geplant, max_length=20)
    # Geplanter Start des Ressouchenplans
    startdatum = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)
    # Anzahl der Tage für die Dauer des Ressouchenplanes, Deafult ist 2 Tage
    anzahlTage = models.IntegerField(default=2)


    # Prüfung ob Ressoucenplan Aktiv
    @property
    def inPlan(self):
        if self.planstatus=='Laufend':
            end_time = self.startdatum + timedelta(days=self.anzahlTage)
            if timezone.now() >= self.startdatum and timezone.now() <= end_time:
                return True

            else:
                return False







# TestTabelle für OPC UA Server
class Test(models.Model):
    # eindeutige ID für den Test
    testnummer = models.PositiveSmallIntegerField(default=0, unique=True)
    Temperature =models.IntegerField(default=0)
    Pressure = models.IntegerField(default=0)
    TIME_Value = models.DateTimeField(auto_now=False, null=True, auto_now_add=False)
