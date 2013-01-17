# -*- coding: utf-8 -*-

import ho.pisa as pisa
import cStringIO as StringIO
from django.template.loader import render_to_string

import csv
from forms import *
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import codecs

from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import letter,A4,A5,A3

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
	if 'buscar' in request.GET:
		search = request.GET['buscar']
		results = colegio.objects.filter(nombre__contains = search.upper())[:10]
		return render_to_response('search.jade',{ 'results' : results },context_instance=RequestContext(request))		
	else:
		if 'id' in request.GET:
			search = request.GET['id']
			result = colegio.objects.filter(pk= search)
			return render_to_response('search_id.jade',{ 'c' : result },context_instance=RequestContext(request))
		else:
			return render_to_response('index.jade',context_instance=RequestContext(request))		

@login_required
def avanzado_view(request):
	dep= ''
	mun= ''
	zona= ''
	niv= ''
	sec= ''
	mod= ''
	rep = ''
	if request.method == 'POST':
		if 'departamento' in request.POST:
			dep 	=	request.POST['departamento']
		if 'municipio' in request.POST:
			mun 	=	request.POST['municipio']
		if 'zona' in request.POST:
			zona 	=	request.POST['zona']
		if 'niveles' in request.POST:
			niv 	=	request.POST['niveles']
		if 'sector' in request.POST:
			sec 	=	request.POST['sector']
		if 'modelos' in request.POST:
			mod 	=	request.POST['modelos']
		if 'reporte' in request.POST:
			rep 	=	request.POST['reporte']

		cols = colegio.objects.filter(departamento=dep.upper() )
		if mun != '':
			cols = cols.filter(municipio=mun.upper() )
		if zona != '':
			cols = cols.filter(zona=zona.upper() )
		if niv != '':
			for n in niv:
				cols = cols.filter(niveles__contains=n.upper() )
		if sec != '':
			cols = cols.filter(sector=sec.upper() )
		if mod != '':
			for m in mod:
				cols = cols.filter(modelos_educativos__contains=m.upper() )
		
#		response = HttpResponse(mimetype='application/pdf')
#		response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#		p = canvas.Canvas(response,pagesize=letter)
#		d = ''
#		cont = 1
	#	for data in cols:
	#		p.line(30,30,550,30)
	#		p.line(30,700,550,700)
#
#			p.drawString(100, 720, data.nombre)
#			p.drawString(370, 720, "Codigo: " + str(data.codigo))
#			p.drawString(50, 680, "Secretaria: " + data.secretaria)
#			p.drawString(190, 680, "Departamento: " + data.cod_dep + "-" + data.departamento)
#			p.drawString(370, 680, "Municipio: " + data.cod_mun + "-" + data.municipio)
#			p.drawString(50, 660, "Dirección: " + str(data.direccion))
#			p.drawString(370, 660, "Telefono: " + data.telefono)
#			p.drawString(50, 640, "Rector: " + data.rector)
#			p.drawString(370, 640, "Tipo: " + data.tipo)
#			p.drawString(50, 620, "Sector: " + data.sector)
#			p.drawString(370, 620, "Zona: " + data.zona)
#			p.drawString(50, 600, "Jornada: " + data.jornadas)
#			p.drawString(50, 580, "Niveles: " + data.niveles)
#			p.drawString(50, 560, "Grados: " + data.grados)
#			p.drawString(50, 540, "Modelos Educativos: " + data.modelos_educativos)
#			p.drawString(50, 520, "Capacidades Exepcionales: ")
#			p.drawString(60, 500, data.capacidades_excepcionales)
#			p.drawString(50, 460, "Discapacidades: ")
#			p.drawString(60, 440, data.discapacidades)
#			p.drawString(50, 400, "Idiomas: ")
#			p.drawString(60, 380, data.idiomas)
#			p.drawString(50, 360, "Numero De Sedes: "+data.numero_sedes )
#			p.drawString(190, 340, "Estado: " + data.estado )
#			p.drawString(370, 340, "Calendario: " + data.calendario )
#			p.drawString(50, 320, "E-mail: "+data.email )

#			p.drawString(50, 50, str(cont))
#			p.showPage()
#			cont = cont + 1

#		p.save()

#		return response

		html = render_to_string('pdf.html',{ 'pagesize':'A4', 'cols': cols },context_instance=RequestContext(request))		
		return  generar_pdf(html)
	else:
		departamentos 	=	Departamento.objects.all()
		municipios		=	Municipio.objects.filter(id=1).order_by('nombre')
		return render_to_response('avanzado.jade',{ 'departamentos':departamentos,'municipios':municipios },context_instance=RequestContext(request))		

@login_required
def upload_view(request):
	if request.method == 'POST':
		if 'file' in request.FILES:
			fcsv = csv.reader( codecs.EncodedFile(request.FILES["file"],"UTF-8",errors='ignore') , delimiter=';')
			for row in fcsv:
				if row[0] != ' Secretaría':
					c = colegio()
					c.secretaria					=		row[0]
					c.cod_dep						=		row[1]
					c.departamento					=		row[2]
					c.cod_mun						=		row[3]
					c.municipio						=		row[4]
					c.codigo						=		row[5]
					c.nombre						=		row[6]
					c.direccion						=		row[7]
					c.telefono						=		row[8]
					c.rector						=		row[9]
					c.tipo							=		row[10]
					c.sector						=		row[11]
					c.zona							=		row[12]
					c.jornadas						=		row[13]
					c.niveles						=		row[14]
					c.grados						=		row[15]
					c.modelos_educativos			=		row[16]
					c.capacidades_excepcionales		=		row[17]
					c.discapacidades				=		row[18]
					c.idiomas						=		row[19]
					c.numero_sedes					=		row[20]
					c.estado						=		row[21]
					c.calendario					=		row[22]
					c.email							=		row[23]
					c.save()
		#return render_to_response('lista.jade',{ 'colegios' : col },context_instance=RequestContext(request))		
		return HttpResponseRedirect('/schools/')	
	return render_to_response('upload.jade',{ 'form' : UploadForm },context_instance=RequestContext(request))

def generar_pdf(html):
	# Función para generar el archivo PDF y devolverlo mediante HttpResponse
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))