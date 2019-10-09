from django.contrib import admin
from .models import VirtuelleOpcUaServer,DienstVirtOpcUaServer, RegOpcUaServer, DienstOpcUaServer,Dienstleistungen,\
DieIntProdukt, IntProdukt, Kunden, ProduktionsAuftrag

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