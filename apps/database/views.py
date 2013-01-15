# -*- encoding: utf-8 -*-
import csv
from forms import *
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import codecs

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
	return render_to_response('avanzado.jade',context_instance=RequestContext(request))		

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