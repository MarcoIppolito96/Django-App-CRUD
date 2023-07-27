from django.contrib import admin
from .models import Task #Importo la clase Task creada en models para poder verla en el panel de administrador

# Esto es para agregar al panel de la tarea, La fecha de CREACION de la misma
class TaskAdmin(admin.ModelAdmin): # Hereda lo que tiene ModelAdmin
    readonly_fields = ('fecha_creacion', ) #readonly_fields Es para decirle cuales campos son de solo lectura y quiero ver en pantalla (va la coma por que es una tupla)
    
# Register your models here.

admin.site.register(Task, TaskAdmin)