from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .form import TaskForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'formulario': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Register usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'formulario': UserCreationForm,
                    "error": "El usuario ya existe"
            })

        return render(request, 'signup.html', {
            'formulario': UserCreationForm,
            "error": "La contraseña no coincide"
        })

@login_required
def tasks(request):
    tasks = Tarea.objects.filter(user=request.user, datecompleted__isnull=True)#esto me devuelve las tareas guardadas del mismo usuario
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def tareas_completadas(request):
    tasks = Tarea.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'created_tasks.html', {
        'formulario': TaskForm
    })
    else:
        try:
            formulario = TaskForm(request.POST)
            new_task = formulario.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'created_tasks.html',{
                'formulario': TaskForm,
                'error': 'Ingrese datos validos'
            })

@login_required
def task_detail(request, tarea_id):
    if request.method == 'GET':
        task = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'tarea': task, 'formulario': form})
    else:
        try:
            task = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'tarea': task, 'formulario': form,'error': 'Error al actualizar la tarea.'})

@login_required        
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.datecompleted = timezone.now()
        tarea.save()
        return redirect('tasks')

@login_required    
def Eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tasks')

@login_required
def CerrarSesion(request):
    logout(request)
    return redirect('home')

def IniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'formulario': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'formulario': AuthenticationForm,
                'error': 'El usuario o la contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('tasks')