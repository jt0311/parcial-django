from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TareasForm
from .models import Tareas
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_view(request):

    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST
                    ['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'login.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
        return render(request, 'login.html', {
            'form': UserCreationForm,
            'error': 'Password no coincide'
        })

@login_required
def tareas(request):
    tareas = Tareas.objects.filter(user=request.user, datecomplete__isnull=True)
    return render(request, 'tareas.html', {'tareas': tareas})

@login_required
def tareas_completas(request):
    tareas = Tareas.objects.filter(user=request.user, datecomplete__isnull=False).order_by('-datecomplete')

    return render(request, 'tareas.html', {'tareas': tareas})


@login_required
def crear_tareas(request):

    if request.method == 'GET':
        return render(request, 'crear_tareas.html', {
            'form': TareasForm
        })
    else:
        try:
            form = TareasForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect(tareas)
        except ValueError:
            return render(request, 'crear_tareas.html',{
                'form': TareasForm,
                'error': 'por favor ingrese datos validos'
            })


@login_required
def tarea_detallada(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
        form = TareasForm(instance=tarea)
        return render(request, 'tarea_detallada.html',{'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
            form = TareasForm(request.POST, instance=tarea)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'tarea_detallada.html',{'tarea': tarea, 'form': form,
            'error': "Error al Actualizar la tarea"})

@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.datecomplete = timezone.now()
        tarea.save()
        return redirect(tareas)

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect(tareas)


@login_required
def cerrar(request):
    logout(request)
    return redirect('home')

@login_required
def buscar(request):
    query = request.GET.get('q') 

    resultados = []
    if query:
        resultados = Tareas.objects.filter(title__icontains=query, user=request.user)

    context = {
        'query': query,
        'resultados': resultados,
    }

    return render(request, 'buscar.html', context)




def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesion.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST
        ['password'])
        if user is None:
            return render(request, 'inicio_sesion.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('tareas')

