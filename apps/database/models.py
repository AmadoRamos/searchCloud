from django.db import models


class colegio(models.Model):
	secretaria			=		models.CharField(max_length=200)
	cod_dep				=		models.CharField(max_length=200)
	departamento		=		models.CharField(max_length=200)
	cod_mun				=		models.CharField(max_length=200)
	municipio			=		models.CharField(max_length=200)
	codigo				=		models.CharField(max_length=200)
	nombre				=		models.CharField(max_length=200)
	direccion			=		models.CharField(max_length=200)
	telefono			=		models.CharField(max_length=200)
	rector				=		models.CharField(max_length=200)
	tipo				=		models.CharField(max_length=200)
	sector				=		models.CharField(max_length=200)
	zona				=		models.CharField(max_length=200)
	jornadas			=		models.CharField(max_length=200)
	niveles				=		models.CharField(max_length=200)
	grados				=		models.CharField(max_length=200)
	modelos_educativos	=		models.TextField()
	capacidades_excepcionales	=		models.CharField(max_length=200)
	discapacidades		=		models.TextField()
	idiomas				=		models.CharField(max_length=200)
	numero_sedes		=		models.CharField(max_length=200)
	estado				=		models.CharField(max_length=200)
	calendario			=		models.CharField(max_length=200)
	email				=		models.EmailField(max_length=200)
	

	def __unicode__(self):
		return (self.nombre)

class Departamento(models.Model):
	nombre				=		models.CharField(max_length=200)

class Municipio(models.Model):
	nombre				=		models.CharField(max_length=200)
	departamento_id		=		models.ForeignKey(Departamento)