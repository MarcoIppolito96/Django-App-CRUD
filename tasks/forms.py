from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descripcion', 'important']
        # Esto es para establecer un estilo directamente en la clase. Así se hace 
        widgets = { 
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }
