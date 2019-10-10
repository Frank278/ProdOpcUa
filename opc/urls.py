from django.urls import path

from .views import *

app_name = 'opc'
urlpatterns = [
    # wenn eine Anfrage an / reinkommt, dann übergebe das der Funktion
    # index aus der views.py
    # zuerst die Authentifizierung
    path('', index, name='index'),
    path("register", register, name="register"),
    path("logout", logout_request, name="logout"),
    path("login", login_request, name="login"),

    # Die Übersichtsseiten der Produktion und der Maschinen
    path('produktion', produktion, name='produktion'),
    path('maschinen', maschinen, name='maschinen'),

    # Die Unterseiten von Produktion und Maschinen
    # Maschinen werden durch OPC UA Server oder virtuelle OPC UA Server simuliert.
    # Die Dienstleistungen, also von den Maschinen ausführbare Arbeiten werden ins Produktionssystem aufgenommen
    # Damit werden dann die Produkte erstellt und die Produktionsaufträge überwacht und optimiert

    # Produktionsaufträge
    path('produktionsAuftrag', produktionsAuftrag_list, name='produktionsAuftrag'),
    # Produkte
    path('intProdukt', intProdukt_list, name='intProdukt'),
    # Benötigte Dienstleistungen bzw. Arbeiten um das Produkt zu erstellen
    path('dieIntProdukt', dieIntProdukt_list, name='dieIntProdukt'),
    # Von den Maschinen zur verfügung gestellte Dienstleistungen
    path('dienstleistungen', dienstleistungen_list, name='dienstleistungen'),

    # Die Maschienen werden durch OPC UA und virtuelle OPC Ua Server ersetzt

    # Die OPC UA Server
    path('regOpcUaServer', regOpcUaServer_list, name='regOpcUaServer'),
    # Von den OPC UA Server zur verfügung gestellte Dienstleistungen
    path('dienstOpcUaServer', dienstOpcUaServer_list, name='dienstOpcUaServer'),

    # Die virtuellen OPC UA Server
    path('virtuelleOpcUaServer', virtuelleOpcUaServer_list, name='virtuelleOpcUaServer'),

    # Von den virtuellen OPC UA Server zur verfügung gestellte Dienstleistungen
    path('dieVirtOpcUaServer', dienstVirtOpcUaServer_list, name='dieVirtOpcUaServer'),

    # Virtuellen OPC UA Server erstellen
    path('virtServerErstellen', virtServerErstellen, name='virtServerErstellen'),

    # Produktionsauftrag erstellen
    path('produktionsAuftragErstellen', produktionsAuftragErstellen, name='produktionsAuftragErstellen'),

    # ProduktionsaÜberwachung
    path('produktionsUeberwachung', prouktionsUeberwachung, name='produktionsUeberwachung'),

]
