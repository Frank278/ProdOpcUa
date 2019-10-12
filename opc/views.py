from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.db import models

# Create your models here.
from django.shortcuts import render, get_object_or_404

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from django.contrib.auth.models import User

from django.urls import reverse
from django.views import generic
from .forms import NewUserForm

from django.contrib import messages

from .models import *


def index(request):
    # context = {'hotelbuchungen': Buchung.objects.all(), 'titel': "Hotelbuchungen"}
    return render(request=request,
                  template_name='main/index.html')


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


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("opc:index")


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


# Erstellen der Datenbankabfrage für die VirtuelleOpcUaServer

@login_required
def virtuelleOpcUaServer_list(request, template_name='main/opcvirtuelleOpcUaServer.html'):
    virtuelleOpcUaServer = VirtuelleOpcUaServer.objects.all()

    data = {}
    data['object_list'] = virtuelleOpcUaServer

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für die DienstVirtOpcUaServer

@login_required
def dienstVirtOpcUaServer_list(request, template_name='main/opcdienstVirtOpcUaServer.html'):
    dienstVirtOpcUaServer = DienstVirtOpcUaServer.objects.all()

    data = {}
    data['object_list'] = dienstVirtOpcUaServer

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für RegOpcUaServer

@login_required
def regOpcUaServer_list(request, template_name='main/opcregOpcUaServer.html'):
    regOpcUaServer = RegOpcUaServer.objects.all()

    data = {}
    data['object_list'] = regOpcUaServer

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für DienstOpcUaServer

@login_required
def dienstOpcUaServer_list(request, template_name='main/opcdienstOpcUaServer.html'):
    dienstOpcUaServer = DienstOpcUaServer.objects.all()

    data = {}
    data['object_list'] = dienstOpcUaServer

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für die Dienstleistungen

@login_required
def dienstleistungen_list(request, template_name='main/opcdienstleistungen.html'):
    dienstleistungen = Dienstleistungen.objects.all()

    data = {}
    data['object_list'] = dienstleistungen

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für die DieIntProdukt

@login_required
def dieIntProdukt_list(request, template_name='main/opcdieIntProdukt.html'):
    dieIntProdukt = DieIntProdukt.objects.all()

    data = {}
    data['object_list'] = dieIntProdukt

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für IntProdukt

@login_required
def intProdukt_list(request, template_name='main/opcintProdukt.html'):
    intProdukt = IntProdukt.objects.all()

    data = {}
    data['object_list'] = intProdukt

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für die Kunden

@login_required
def kunden_list(request, template_name='main/opckunden.html'):
    kunden = Kunden.objects.all()

    data = {}
    data['object_list'] = kunden

    return render(request, template_name, data)


# Erstellen der Datenbankabfrage für ProduktionsAuftrag

@login_required
def produktionsAuftrag_list(request, template_name='main/opcproduktionsAuftrag.html'):
    produktionsAuftrag = ProduktionsAuftrag.objects.all()

    data = {}
    data['object_list'] = produktionsAuftrag

    return render(request, template_name, data)

# Erstellen der Datenbankabfrage für DienstOpcUaServer

@login_required
def ressourcenplanung_list(request, template_name='main/opcressourcen.html'):
    ressourcenplanung = Ressourcenplanung.objects.all()

    data = {}
    data['object_list'] = ressourcenplanung

    return render(request, template_name, data)


# Erstellen von Virtuellen Servern
@login_required
def virtServerErstellen(request):
    return render(request=request,
                  template_name='main/opcvirtServerErstellen.html')

# Erstellen von Produktionsaufträgen
@login_required
def produktionsAuftragErstellen(request):
    return render(request=request,
                  template_name='main/opcproduktionsAuftragErstellen.html')

# Hinzufügen von Servern
@login_required
def serverHinzu(request):
    return render(request=request,
                  template_name='main/opcserverHinzu.html')


# Produktionsüberwachung
@login_required
def prouktionsUeberwachung(request):
    return render(request=request,
                  template_name='main/opcproduktionsUeberwachung.html')