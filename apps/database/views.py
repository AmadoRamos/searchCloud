# -*- coding: utf-8 -*-

import ho.pisa as pisa
import cStringIO as StringIO

import csv
from forms import *
from models import *

from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import codecs

from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import letter,A4,A5,A3


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
	dep			= 		''
	mun			= 		''
	zona		= 		''
	niv			= 		''
	sec			= 		''
	mod			= 		''
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

		cols = colegio.objects.filter(departamento=dep.upper() )
		if mun != '':
			cols = cols.filter(municipio__contains=mun.upper() )
		if zona != '':
			cols = cols.filter(zona=zona.upper() )
		if niv != '':
			for n in niv:
				cols = cols.filter(niveles__contains=n.upper() )
		if sec != '':
			cols = cols.filter(sector__exact=sec.upper() )
		if mod != '':
			for m in mod:
				cols = cols.filter(modelos_educativos__contains=m.upper() )

		html = render_to_string('pdf.html',{ 'pagesize':'A4', 'cols': cols, 'reporte' : request.POST.getlist('reporte[]') },context_instance=RequestContext(request))		
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

@login_required
@csrf_exempt
def ajax_view(request):
	if request.is_ajax():
		if request.method == 'POST':
			m 	= 	Municipio.objects.filter(departamento_id_id= request.POST['departamento'])
			return render_to_response('ajax.jade',{ 'datos' : m },context_instance=RequestContext(request))