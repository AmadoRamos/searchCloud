from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.database.views',
	url(r'^upload','upload_view',name='upload_principal'),
	url(r'^avanzado','avanzado_view',name='avanzado_principal'),
	url(r'^','index_view',name='vista_principal'),
)