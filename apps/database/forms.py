# -*- coding: utf-8 -*-
from django import forms


class UploadForm(forms.Form):
	file = forms.FileField()