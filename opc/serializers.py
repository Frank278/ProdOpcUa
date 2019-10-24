from django.contrib.auth.models import User, Group
from rest_framework import serializers

import opc, objects
from .models import *
from rest_framework import serializers



class ProduktionsAuftragSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProduktionsAuftrag
        fields = ['auftragsnummer', 'anzahlSchritte', 'auftragsstatus']






