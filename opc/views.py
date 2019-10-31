from django.shortcuts import render

# Create your views here.
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic, View
from .forms import NewUserForm
from django.db.models import Count
from tablib import Dataset

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
import json
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import *

from .models import *

# Hauptseite
def index(request):
    return render(request=request,
                  template_name='main/index.html')

# Seite zum Registrieren
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("opc:index")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})

# Abmeldung und Rückkehr zur Haauptseite
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("opc:index")

# Anmeldung und Rückkehr zur Hauptseite
# Es wird ein Toast mit einer Nachricht ausgegeben
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.info(request, f"You are now logged in as {username}")
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


# Erstellen der Übersichtseite für die Produktion
@login_required
def produktion(request):
    return render(request=request,
                  template_name='main/produktion.html')


# Erstellen der Übersichtseite für die Maschinen
@login_required
def maschinen(request):
    return render(request=request,
                  template_name='main/maschinen.html')


# Erstellen der Datenbankabfrage für die OpcUaServer
@login_required
def regOpcUaServer_list(request, template_name='main/opcregOpcUaServer.html'):
    regOpcUaServer = RegOpcUaServer.objects.all()

    data = {}
    data['object_list'] = regOpcUaServer

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für Dienstleistungen
@login_required
def dienstleistungen_list(request, template_name='main/opcdienstleistungen.html'):
    dienstleistungen = Dienstleistungen.objects.all()

    data = {}
    data['object_list'] = dienstleistungen

    return render(request, template_name, data)



# Erstellen der Datenbankabfrage für die Produkte
@login_required
def produkt_list(request, template_name='main/opcProdukt.html'):
    produkt = Produkt.objects.all()

    data = {}
    data['object_list'] = produkt

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für die Kunden
@method_decorator(login_required, name='dispatch')
class kundenList(ListView):
    template_name='main/opckunden.html'
    Model = Kunden
    def get_queryset(self):
        return Kunden.objects.all()



# Erstellen der Datenbankabfrage für ProduktionsAuftrag
@method_decorator(login_required, name='dispatch')
class produktionsAuftragList(ListView):
    template_name='main/opcproduktionsAuftrag.html'
    Model = ProduktionsAuftrag
    def get_queryset(self):
        return ProduktionsAuftrag.objects.all()


# Erstellen der Datenbankabfrage für die Ressourcenplannung
@method_decorator(login_required, name='dispatch')
class ressourcenplanungList(ListView):
    template_name='main/opcressourcen.html'
    def get_queryset(self):
        return Ressourcenplanung.objects.all()



# Erstellen der Ansicht der serverdaten
@method_decorator(login_required, name='dispatch')
class serverdataView(ListView):
    template_name='main/serverdata.html'
    Model = Serverdata

    def get_queryset(self):
        return Serverdata.objects.all()





# Erstellen von Produktionsaufträgen
@login_required
def produktionsAuftragErstellen(request):
    return render(request=request,
                  template_name='main/opcproduktionsAuftragErstellen.html')


# Produktionsüberwachung
@login_required
def produktionsUeberwachung_list(request, template_name='main/opcproduktionsUeberwachung.html'):
    produktionsAuftrag = ProduktionsAuftrag.objects.all().order_by('auftragseingang', 'auftragsstatus',)
    anzahlauftraege = ProduktionsAuftrag.objects.count()

    wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
    auslastung = [80, 70, 90, 80, 70, 60, 60],
    #auftragszeiten = Produkt.objects.all().aggregate(Count('erstellungszeit'))
    auftragszeiten = Produkt.objects.all()
    anzahlserver = RegOpcUaServer.objects.count()
    anzahlprodukte = Produkt.objects.count()

    produkt = [obj.produkt for obj in produktionsAuftrag]
    auftragsmenge = [int(obj.auftragsmenge) for obj in produktionsAuftrag]

    maschinetime = anzahlserver * timedelta(days=1)

    context = {
        'produkt': produkt,
        'auftragsmenge': auftragsmenge,
        'produktionsAuftrag': produktionsAuftrag,
        'auftragszeiten': auftragszeiten,
        'anzahlauftraege': anzahlauftraege,
        'anzahlserver': anzahlserver,
        'wochentage': wochentage,
        'auslastung': auslastung,
        'maschinetime': maschinetime,
        'anzahlprodukte': anzahlprodukte,
        'list_produktionsAuftrag':produktionsAuftrag,
    }


    return render(request, template_name, context)







#Für REST API zum export und Import der Daten

class RegOpcUaServerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RegOpcUaServer.objects.all()
    serializer_class = RegOpcUaServerSerializer

class DienstleistungenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dienstleistungen.objects.all()
    serializer_class = DienstleistungenSerializer

class KundenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Kunden.objects.all()
    serializer_class = KundenSerializer


class ProduktViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer

class ProduktAuftragViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProduktionsAuftrag.objects.all()
    serializer_class = ProduktionsAuftragSerializer

class RessourcenplanungViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Ressourcenplanung.objects.all()
    serializer_class = RessourcenplanungSerializer

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='main/chart.html')
line_chart_json = LineChartJSONView.as_view()
