from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from decimal import Decimal
from django.contrib.auth.models import Group, Permission, User
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Indenter
from datetime import *
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from SGP import settings
from proyecto.models import Userstory, ProyectoFlujoActividad, Proyecto, FlujoProyecto, Sprint
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.units import inch
import decimal
import  json
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Cantidad de trabajos por usuario pendiente, en curso, finalizados
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usUsuario():
    '''
    Funcion que genera el reporte de cantidad de trabajos por usuario pendiente, en curso, finalizados
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usUsuario.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>UserStories por Usuario<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los usuarios activos del sistema
    '''
    usuarios= User.objects.filter(is_active=True)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    for usr in usuarios:
            userstories = Userstory.objects.filter(usuarioasignado = usr)
            if userstories:
                #escribir el contador
                Story.append(Indenter(25))
                text="<strong>"+str(contador_act)+".</strong>"
                Story.append(Paragraph(text, styles["Subtitulos"]))

                #escribir el nombre de la persona
                text ="<strong>Nombre: </strong>" + str(usr.username) +"<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-25))

                for us in userstories:
                    #escribir su nombre userstory, estado y nombre proyecto
                    Story.append(Indenter(42))
                    Story.append(Spacer(1, 10))
                    text ="<strong> * User story: </strong>" + us.nombre + "&nbsp;&nbsp;&nbsp;&nbsp;"+ "<strong>Estado: </strong>"+ us.estado+ "&nbsp;&nbsp;&nbsp;&nbsp;"+ "<strong>Proyecto: </strong>"+us.sprint.proyecto.nombre+"<br>"
                    Story.append(Paragraph(text, styles["SubItems"]))
                    Story.append(Indenter(-42))

                Story.append(Indenter(25))
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Spacer(1, 12))
                Story.append(Indenter(-25))
                contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usUsuario.pdf"

def descargar_reporte_us_usuario(request):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usUsuario())

    return StreamingHttpResponse(a,content_type='application/pdf')



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            Cantidad de trabajos en curso por equipo
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usXProyecto():
    '''
    Funcion que genera el reporte de cantidad de trabajos en curso por equipo
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usXProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>UserStories en Curso por Proyecto<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyectos= Proyecto.objects.filter(is_active=True)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    for pr in proyectos:
            #lista de us del proyecto
            lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=pr.pk)

            #si el proyecto tiene users
            if lista_flujo_actividad:
                #escribir el contador
                Story.append(Indenter(25))
                text="<strong>"+str(contador_act)+".</strong>"
                Story.append(Paragraph(text, styles["Subtitulos"]))

                #escribir el nombre del Proyecto
                text ="<strong>Proyecto: </strong>" + str(pr.nombre) +"<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-25))

                for fa in lista_flujo_actividad:
                  if fa.userstory.estado == 'EnCurso':
                    #listar us de proyecto con estado en curso
                    Story.append(Indenter(42))
                    Story.append(Spacer(1, 10))
                    text ="<strong> * </strong>" + fa.userstory.nombre +"<br>"
                    Story.append(Paragraph(text, styles["SubItems"]))
                    Story.append(Indenter(-42))

                Story.append(Indenter(25))
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Spacer(1, 12))
                Story.append(Indenter(-25))
                contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usXProyecto.pdf"

def descargar_reporte_usXProyecto(request):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usXProyecto())

    return StreamingHttpResponse(a,content_type='application/pdf')



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Lista clasificada por orden de prioridad de todas las actividades  para completar un proyecto.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_actividadesXProyecto():
    '''
    Funcion que genera el reporte de todas las actividades  para completar un proyecto.
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_actividadesXProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Actividades Ordenadas por Proyecto<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyectos= Proyecto.objects.filter(is_active=True)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    for pr in proyectos:
            #lista de proyecto_flujo_actividad del proyecto
            lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=pr.pk)

            #si el proyecto tiene users
            if lista_flujo_actividad:
                #escribir el contador
                Story.append(Indenter(25))
                text="<strong>"+str(contador_act)+".</strong>"
                Story.append(Paragraph(text, styles["Subtitulos"]))

                #escribir el nombre del Proyecto
                text ="<strong>Proyecto: </strong>" + str(pr.nombre) +"<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-25))
                nombreus= ''
                for fa in lista_flujo_actividad:
                    #listar us de proyecto con sus actividades
                    if nombreus!= fa.userstory.nombre:
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> " + fa.userstory.nombre +" </strong>"+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                        nombreus = fa.userstory.nombre
                    #actividades
                    Story.append(Indenter(42))
                    Story.append(Spacer(1, 10))
                    text ="<strong> * </strong>"+ str(fa.flujoActividad.orden)+ "&nbsp;&nbsp;&nbsp;&nbsp;"+  fa.flujoActividad.actividad.nombre + "<br>"
                    Story.append(Paragraph(text, styles["SubItems"]))
                    Story.append(Indenter(-42))


                Story.append(Indenter(25))
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Spacer(1, 12))
                Story.append(Indenter(-25))
                contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_actividadesXProyecto.pdf"

def descargar_reporte_actividadesXProyecto(request):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_actividadesXProyecto())

    return StreamingHttpResponse(a,content_type='application/pdf')




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# El Backlog del Producto, lista ordenada de HU, en el orden que esperamos deban terminarse
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usOrdenadoXProyecto():
    '''
    Funcion que genera el reporte de todos los US ordenados por prioridad de cada US
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usOrdenadoXProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>User Stories ordenados por prioridad<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyectos= Proyecto.objects.filter(is_active=True)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    for pr in proyectos:
            #lista de proyecto_flujo_actividad del proyecto
            lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=pr.pk)

            #si el proyecto tiene users
            if lista_flujo_actividad:
                #escribir el contador
                Story.append(Indenter(25))
                text="<strong>"+str(contador_act)+".</strong>"
                Story.append(Paragraph(text, styles["Subtitulos"]))

                #escribir el nombre del Proyecto
                text ="<strong>Proyecto: </strong>" + str(pr.nombre) +"<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-25))
                prioridadAlta= []
                prioridadNormal= []
                prioridadBaja= []
                #Separar userstories por Prioridad
                nombreus= ''
                for fa in lista_flujo_actividad:
                    if fa.userstory.prioridad == 'Alta':
                        if nombreus != fa.userstory.nombre:
                            prioridadAlta.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                    elif fa.userstory.prioridad == 'Normal':
                         if nombreus != fa.userstory.nombre:
                            prioridadNormal.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                    elif fa.userstory.prioridad == 'Baja':
                         if nombreus != fa.userstory.nombre:
                            prioridadBaja.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                if prioridadAlta:
                    #listar us de prioridad Alta
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Alta </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for alta in prioridadAlta:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(alta)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                if prioridadNormal:
                    #listar us de prioridad Normal
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Normal </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for normal in prioridadNormal:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(normal)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                if prioridadBaja:
                    #listar us de prioridad Baja
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Baja </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for baja in prioridadBaja:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(baja)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                Story.append(Indenter(25))
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Spacer(1, 12))
                Story.append(Indenter(-25))
                contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usOrdenadoXProyecto.pdf"

def descargar_reporte_usOrdenadoXProyecto(request):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usOrdenadoXProyecto())

    return StreamingHttpResponse(a,content_type='application/pdf')



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#El Backlog del Sprin, lista de los elementos del Backlog del Producto, elegidos para ser desarrollador en el Sprint actual
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usSprintActualXProyecto():
    '''
    Funcion que genera el reporte de todos los US del sprint actual por proyecto
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usSprintActualXProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>User Stories del Sprint Activo<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyectos= Proyecto.objects.filter(is_active=True)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    for pr in proyectos:
            existeActivoFlujoProyecto = FlujoProyecto.objects.filter(proyecto_id=pr.pk, estado='Doing').exists()
            if existeActivoFlujoProyecto:
                activoFlujoProyecto = FlujoProyecto.objects.get(proyecto_id=pr.pk, estado='Doing')
                sprintActivo = Sprint.objects.get(id=activoFlujoProyecto.sprint.pk)
                userStories = Userstory.objects.filter(sprint_id=sprintActivo.id)
                #escribir el contador
                Story.append(Indenter(25))
                text="<strong>"+str(contador_act)+".</strong>"
                Story.append(Paragraph(text, styles["Subtitulos"]))

                #escribir el nombre del Proyecto
                text ="<strong>Proyecto: </strong>" + str(pr.nombre) +"<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-25))

                #escribir el nombre del sprint activo
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="<strong> Sprint Activo: " + sprintActivo.nombre +" </strong>"+ "<br>"
                Story.append(Paragraph(text, styles["SubItems"]))


                for us in userStories:
                    #userstories del sprint activo
                    Story.append(Indenter(42))
                    Story.append(Spacer(1, 10))
                    text ="<strong> * User Story: </strong>"+ us.nombre+ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" +"<strong> Estado: </strong>" + us.estado+ "<br>"
                    Story.append(Paragraph(text, styles["SubItems"]))
                    Story.append(Indenter(-42))

                Story.append(Indenter(-42))
                Story.append(Indenter(25))
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Spacer(1, 12))
                Story.append(Indenter(-25))
                contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usSprintActualXProyecto.pdf"

def descargar_reporte_usSprintActualXProyecto(request):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usSprintActualXProyecto())

    return StreamingHttpResponse(a,content_type='application/pdf')

'''
Prueba
'''

def reporte(id_proyecto):
    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/test.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)
    story = []

    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    story.append(im)
    titulo="<b>Grafico de Sprint por Proyecto<br/>"
    story.append(Paragraph(titulo,styles['Principal']))
    story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    story.append(Spacer(0, inch*.1))
    '''
        Codigo de Sprint por US
    '''
    sprint = Sprint.objects.filter(proyecto_id=id_proyecto)
    ejeXName = []
    ejeXValor = []
    duracionOptimaX = []

    for sp in sprint:
       ejeXName.append(sp.nombre)
       dec = Decimal(sp.tiempoacumulado)
       ejeXValor.append(format(dec, '.2f'))
       duracionOptimaX.append(sp.duracion)

    d = Drawing(400, 200)
    lc = HorizontalLineChart()
    lc.x = 30
    lc.y = 50
    lc.height = 125
    lc.width = 350
    #lc.data = [[0.5,1.5]]
    #lc.data = ejeXValor




    #lc.categoryAxis.categoryNames = ['Suspenso', 'Aprobado', 'Notable',
                                    #'Sobresaliente']
    lc.categoryAxis.categoryNames = ejeXName
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 2.5
    lc.valueAxis.valueStep = 0.5
    lc.lines[0].strokeWidth = 2
    lc.lines[0].symbol = makeMarker('FilledCircle')
    lc.lines[1].strokeWidth = 1.5
    d.add(lc)
    story.append(d)
    doc.build(story)
    return str(settings.BASE_DIR)+"/test.pdf"

def descargar_reporte_(request,id_proyecto):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')


##################################################################################################################
'''
    Metodos de reportes con el id de proyecto
'''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            Cantidad de trabajos en curso por proyecto especificando su id
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usEnCursoIdProyecto(id_proyecto):
    '''
    Funcion que genera el reporte de cantidad de trabajos en curso por equipo
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usEnCursoIdProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>UserStories en Curso<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos el proyecto ingresado
    '''

    proyecto= Proyecto.objects.get(auto_increment_id=id_proyecto)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    #lista de us del proyecto
    lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=id_proyecto)
    #escribir el contador
    Story.append(Indenter(25))
    #escribir el nombre del Proyecto
    text ="<strong>Proyecto: </strong>" + str(proyecto.nombre) +"<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Indenter(-25))
    #si el proyecto tiene users
    if lista_flujo_actividad:
         for fa in lista_flujo_actividad:
             if fa.userstory.estado == 'EnCurso':
                #listar us de proyecto con estado en curso
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="<strong> * </strong>" + fa.userstory.nombre +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
                contador_act+=1
    else:
        Story.append(Indenter(42))
        Story.append(Spacer(1, 10))
        text ="<strong> NO POSEE US EN CURSO </strong>" + "<br>"
        Story.append(Paragraph(text, styles["SubItems"]))
        Story.append(Indenter(-42))

    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usEnCursoIdProyecto.pdf"

def descargar_reporte_usEnCursoIdProyecto(request,id_proyecto):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usEnCursoIdProyecto(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Lista clasificada por orden de prioridad de todas las actividades  para completar ID proyecto.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_actividadesXIDProyecto(id_proyecto):
    '''
    Funcion que genera el reporte de todas las actividades  para completar un proyecto.
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_actividadesXIDProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Actividades Ordenadas por Proyecto<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyecto= Proyecto.objects.get(auto_increment_id=id_proyecto)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))

    #lista de proyecto_flujo_actividad del proyecto
    lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=id_proyecto)
    #escribir el contador
    Story.append(Indenter(25))
    text="<strong>"+str(contador_act)+".</strong>"
    Story.append(Paragraph(text, styles["Subtitulos"]))
    #escribir el nombre del Proyecto
    text ="<strong>Proyecto: </strong>" + str(proyecto.nombre) +"<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Indenter(-25))
    #si el proyecto tiene users
    if lista_flujo_actividad:
          nombreus= ''
          for fa in lista_flujo_actividad:
             #listar us de proyecto con sus actividades
             if nombreus!= fa.userstory.nombre:
                 Story.append(Indenter(42))
                 Story.append(Spacer(1, 10))
                 text ="<strong> " + fa.userstory.nombre +" </strong>"+ "<br>"
                 Story.append(Paragraph(text, styles["SubItems"]))
                 Story.append(Indenter(-42))
                 nombreus = fa.userstory.nombre
                 #actividades
                 Story.append(Indenter(42))
                 Story.append(Spacer(1, 10))
                 text ="<strong> * </strong>"+ str(fa.flujoActividad.orden)+ "&nbsp;&nbsp;&nbsp;&nbsp;"+  fa.flujoActividad.actividad.nombre + "<br>"
                 Story.append(Paragraph(text, styles["SubItems"]))
                 Story.append(Indenter(-42))
    else:
        Story.append(Indenter(42))
        Story.append(Spacer(1, 10))
        text ="<strong> NO POSEE US </strong>" + "<br>"
        Story.append(Paragraph(text, styles["SubItems"]))
        Story.append(Indenter(-42))

    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_actividadesXIDProyecto.pdf"

def descargar_reporte_actividadesXIDProyecto(request,id_proyecto):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_actividadesXIDProyecto(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# El Backlog del Producto, lista ordenada de HU, en el orden que esperamos deban terminarse
# Ingresando el ID de proyecto
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usOrdenadoXIDProyecto(id_proyecto):
    '''
    Funcion que genera el reporte de todos los US ordenados por prioridad de cada US
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usOrdenadoXIDProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>User Stories ordenados por prioridad<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyecto= Proyecto.objects.get(auto_increment_id=id_proyecto)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    #escribir el contador
    Story.append(Indenter(25))
    text="<strong>"+str(contador_act)+".</strong>"
    Story.append(Paragraph(text, styles["Subtitulos"]))
    #escribir el nombre del Proyecto
    text ="<strong>Proyecto: </strong>" + str(proyecto.nombre) +"<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Indenter(-25))

    #lista de proyecto_flujo_actividad del proyecto
    lista_flujo_actividad = ProyectoFlujoActividad.objects.filter(proyecto_id=id_proyecto)
    #si el proyecto tiene users
    if lista_flujo_actividad:

                prioridadAlta= []
                prioridadNormal= []
                prioridadBaja= []
                #Separar userstories por Prioridad
                nombreus= ''
                for fa in lista_flujo_actividad:
                    if fa.userstory.prioridad == 'Alta':
                        if nombreus != fa.userstory.nombre:
                            prioridadAlta.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                    elif fa.userstory.prioridad == 'Normal':
                         if nombreus != fa.userstory.nombre:
                            prioridadNormal.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                    elif fa.userstory.prioridad == 'Baja':
                         if nombreus != fa.userstory.nombre:
                            prioridadBaja.append(fa.userstory.nombre)
                            nombreus = fa.userstory.nombre
                if prioridadAlta:
                    #listar us de prioridad Alta
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Alta </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for alta in prioridadAlta:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(alta)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                if prioridadNormal:
                    #listar us de prioridad Normal
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Normal </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for normal in prioridadNormal:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(normal)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                if prioridadBaja:
                    #listar us de prioridad Baja
                     Story.append(Indenter(42))
                     Story.append(Spacer(1, 10))
                     text ="<strong> US con prioridad Baja </strong>"+ "<br>"
                     Story.append(Paragraph(text, styles["SubItems"]))
                     Story.append(Indenter(-42))
                     for baja in prioridadBaja:
                        #userstories
                        Story.append(Indenter(42))
                        Story.append(Spacer(1, 10))
                        text ="<strong> -- </strong>"+ str(baja)+ "<br>"
                        Story.append(Paragraph(text, styles["SubItems"]))
                        Story.append(Indenter(-42))
                Story.append(Indenter(25))

    else:
        Story.append(Indenter(42))
        Story.append(Spacer(1, 10))
        text ="<strong> NO POSEE US </strong>" + "<br>"
        Story.append(Paragraph(text, styles["SubItems"]))
        Story.append(Indenter(-42))
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usOrdenadoXIDProyecto.pdf"

def descargar_reporte_usOrdenadoXIDProyecto(request,id_proyecto):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usOrdenadoXIDProyecto(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#El Backlog del Sprin, lista de los elementos del Backlog del Producto, elegidos para
# ser desarrollador en el Sprint actual
#ID Proyecto
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def reporte_usSprintActualXIDProyecto(id_proyecto):
    '''
    Funcion que genera el reporte de todos los US del sprint actual por proyecto
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usSprintActualXIDProyecto.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/img/sgp.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>User Stories del Sprint Activo<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    '''
        Obtenemos los proyectos activos del sistema
    '''
    proyecto= Proyecto.objects.get(auto_increment_id=id_proyecto)

    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    Story.append(Indenter(25))
    text="<strong>"+str(contador_act)+".</strong>"
    Story.append(Paragraph(text, styles["Subtitulos"]))
    #escribir el nombre del Proyecto
    text ="<strong>Proyecto: </strong>" + str(proyecto.nombre) +"<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Indenter(-25))
    existeActivoFlujoProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Doing').exists()
    if existeActivoFlujoProyecto:
                activoFlujoProyecto = FlujoProyecto.objects.get(proyecto_id=id_proyecto, estado='Doing')
                sprintActivo = Sprint.objects.get(id=activoFlujoProyecto.sprint.pk)
                userStories = Userstory.objects.filter(sprint_id=sprintActivo.id)
                #escribir el contador


                #escribir el nombre del sprint activo
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="<strong> Sprint Activo: " + sprintActivo.nombre +" </strong>"+ "<br>"
                Story.append(Paragraph(text, styles["SubItems"]))


                for us in userStories:
                    #userstories del sprint activo
                    Story.append(Indenter(42))
                    Story.append(Spacer(1, 10))
                    text ="<strong> * User Story: </strong>"+ us.nombre+ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" +"<strong> Estado: </strong>" + us.estado+ "<br>"
                    Story.append(Paragraph(text, styles["SubItems"]))
                    Story.append(Indenter(-42))
    else:
        Story.append(Indenter(42))
        Story.append(Spacer(1, 10))
        text ="<strong> NO POSEE US </strong>" + "<br>"
        Story.append(Paragraph(text, styles["SubItems"]))
        Story.append(Indenter(-42))

    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usSprintActualXIDProyecto.pdf"

def descargar_reporte_usSprintActualXIDProyecto(request,id_proyecto):
    '''
    Vista para descargar el reporte
    '''
    '''if request.user.is_superuser!=True:
        return render_to_response('extiende.html',context_instance=RequestContext(request))'''
    a=file(reporte_usSprintActualXIDProyecto(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')


def irSeccionReporte(request,id_proyecto):
    template_name = './Proyecto/reportes.html'
    return render(request,template_name,{'id_proyecto':id_proyecto})


def irSeccionReporteGeneral(request):
    template_name = './Proyecto/reportesGenerales.html'
    return render(request,template_name)