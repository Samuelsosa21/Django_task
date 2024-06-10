from django.contrib import admin
from .models import Tarea

class TareasAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here
admin.site.register(Tarea, TareasAdmin)
