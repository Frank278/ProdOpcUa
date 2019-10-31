from django.urls import path

from .views import *
from django.urls import include, path
from rest_framework import routers

# Dem Router das Viewset for den REST API bekannt geben
router = routers.DefaultRouter()
router.register(r'RegOpcUaServer', RegOpcUaServerViewSet)
router.register(r'Dienstleistungen', DienstleistungenViewSet)
router.register(r'Kunden', KundenViewSet)
router.register(r'Produkt', ProduktViewSet)
router.register(r'produktionsauftrag', ProduktAuftragViewSet)
router.register(r'Ressourcenplanung', RessourcenplanungViewSet)



#router.register(r'groups', views.GroupViewSet)

app_name = 'opc'
urlpatterns = [
    # wenn eine Anfrage an / reinkommt, dann übergebe das der Funktion
    # index aus der views.py
    path('', index, name='index'),

    # REST API einbinden
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Die Authentifizierung
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
    path('produktionsAuftrag', produktionsAuftragList.as_view(), name='produktionsAuftrag'),


    # Produkte
    path('Produkt', produkt_list, name='Produkt'),

    # Von den Maschinen zur verfügung gestellte Dienstleistungen
    path('dienstleistungen', dienstleistungen_list, name='dienstleistungen'),

    # Die Maschienen werden durch OPC UA und virtuelle OPC Ua Server ersetzt

    # Die OPC UA Server
    path('regOpcUaServer', regOpcUaServer_list, name='regOpcUaServer'),


    # Produktionsauftrag erstellen
    path('produktionsAuftragErstellen', produktionsAuftragErstellen, name='produktionsAuftragErstellen'),

    # ProduktionsaÜberwachung
    path('produktionsUeberwachung',produktionsUeberwachung_list, name='produktionsUeberwachung'),
   # path('produktionsUeberwachung', prouktionsUeberwachung_list, name='produktionsUeberwachung'),

    # Ressourcenplanung, verteilen der Poduktionsaufträge auf die Maschinen
    path('ressourcenplanung', ressourcenplanungList.as_view(), name='ressourcenplanung'),

    # Anzeige der Kundendaten
    path('kunden', kundenList.as_view(), name='kunden'),

    # Die von den Serern eingehenden Daten
    path('serverdata',serverdataView.as_view(), name='serverdata'),




]