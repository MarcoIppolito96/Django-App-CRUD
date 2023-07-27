from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
    })
    elif request.POST['password1'] == request.POST['password2']:
        #validar considerando posible error de la DB
        try:    
            # registrar usuario
            user = User.objects.create_user(username=request.POST['username'],
            password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('tasks')
        except:
            return render(request, 'signup.html', {
            'form': UserCreationForm,
            'mensaje': 'El usuario ya existe'
    })
    return render(request, 'signup.html', {
        'form': UserCreationForm,
        'mensaje': 'Las contraseñas no coinciden'
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(usuario=request.user, fecha_completado__isnull=True)# (usuario=request.user, fecha_completado__isnull=True) # Con esto mostrariamos las tareas a cada usuario suyas y que no estén completadas
    return render(request,'tasks.html',{
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(usuario=request.user, fecha_completado__isnull=False).order_by('-fecha_completado') #devuelva las tareas completadas ordenando por fecha de completado
    return render(request, 'tasks_completed.html',{
        'tasks' : tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        #Enviar datos del formulario a la DB
        try: 
            form = TaskForm(request.POST) # Le pasamos a la clase Taskform los datos que son mandados desde el FRONT
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TaskForm,
            'error': 'Por favor provee datos válidos'
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, usuario=request.user) #Obtener la tarea por ID para despues pasarla al FRONT, usamos get_object_or_404 para que si se pone un id de una tarea que no existe no se Caiga el servidor(Ademas se filtra por tarea de cada usuario)
        form = TaskForm(instance=task) # Aca la variable form Tiene el modelo de TaskForm, pero con los datos instanciados de la variable en particular task, que es un id VARIABLE para cada tarea
        return render(request,'task_detail.html',{
            'task': task,
            'form': form
        })
    else:
            try:
                task = get_object_or_404(Task, pk=task_id, usuario=request.user)
                form = TaskForm(request.POST, instance=task) # Actualizar la tarea
                form.save()
                return redirect('tasks')
            except ValueError:
                return render(request,'task_detail.html',{
                    'task': task,
                    'form': form,
                    'error': 'Error actualizando la tarea'
                })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user) # Solo las tareas que le pertenecen al usuario
    if request.method == 'POST':
        task.fecha_completado = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user) # Solo las tareas que le pertenecen al usuario
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: #Si la variable user esta vacía
            return render(request,'signin.html',{
            'form': AuthenticationForm,
            'error': 'El usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')