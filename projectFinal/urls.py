"""
URL configuration for projectFinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from parcial import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('tareas/', views.tareas, name='tareas'),
    path('tareas_completed/', views.tareas_completas, name='tareas_completas'),
    path('tareas/create/', views.crear_tareas, name='crear_tareas'),
    path('tareas/<int:tarea_id>/', views.tarea_detallada, name='tarea_detallada'),
    path('tareas/<int:tarea_id>/complete/', views.completar_tarea, name='completar_tarea'),
    path('tareas/<int:tarea_id>/delete/', views.eliminar_tarea, name='eliminar_tarea'),
    path('logout/', views.cerrar, name='cerrar'),
    path('inicio/', views.inicio_sesion, name='inicio'),
    path('buscar/', views.buscar, name='buscar'),
]
