from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(VirtuelleOpcUaServer)
admin.site.register(DienstVirtOpcUaServer)
admin.site.register(RegOpcUaServer)
admin.site.register(DienstOpcUaServer)
admin.site.register(Dienstleistungen)
admin.site.register(DieIntProdukt)
admin.site.register(IntProdukt)
admin.site.register(Kunden)
admin.site.register(ProduktionsAuftrag)
admin.site.register(Ressourcenplanung)