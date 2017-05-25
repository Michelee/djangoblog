from django import forms
from django.contrib import admin
from .models import Post
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
import os
from django.db import models

# class AdminImageWidget(AdminFileWidget): 
# 	def render(self, name, value, attrs=None): 
# 		output = []
# 		if value and hasattr(value, "url"):
# 			output.append(('<a target="_blank" href="%s">'
# 			'<img src="%s" style="height: 250px;" /></a> <br /><br />' % (value.url, value.url)))
# 		output.append(super(AdminImageWidget, self).render(name, value, attrs))
# 		return mark_safe(u''.join(output))

class NewTabAdminFileWidget(AdminFileWidget):
	"""
	This widget is an extensions from AdminFileWidget which is used with all
	ImageFields and FileFields at admin forms. This widget follows the api defined
	by django.forms.widgets.ClearableFileInput widget.
	"""

	def __init__(self, *args, **kwargs):
		super(NewTabAdminFileWidget, self).__init__(*args, **kwargs)
		template_with_initial_new_tab = (
			'%(initial_text)s: <a href="%(initial_url)s" target="_blank">%(initial)s</a> '
			'%(clear_template)s<br />%(input_text)s: %(input)s'
		)

		self.template_with_initial = ('<p class="file-upload">%s</p>' % template_with_initial_new_tab)

# class FileInNewWindowWidget(AdminFileWidget):
# 	# AdminFileWidget inherits from django.forms.ClearableFileInput
# 	# The original url_markup_template in django.forms.ClearableFileInput is:
# 	# url_markup_template = '<a href="{0}">{1}</a>'
# 	url_markup_template = '<a href="{0}" target="_blank">{1}</a>'


# class AttachmentInline(admin.TabularInline):
# 	formfield_overrides = {
# 		models.ImageField: {'widget': FileInNewWindowWidget ()},
# 	}	

class FormatString(str):
	def format(self, *args, **kwargs):
		arguments = list(args)
		arguments[1] = path.basename(arguments[1])
		return super(FormatString, self).format(*arguments, **kwargs)


class ClearableFileInput(forms.ClearableFileInput):
	url_markup_template = FormatString('<a href="{0}" target="_blank">{1}</a>')


class PostModelForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ["slug", "height_field", "width_field"]
		widgets = {
			'image' : NewTabAdminFileWidget()
		}

		def __init__(self, *args, **kwargs):
			super(PostModelForm, self).__init__(*args, **kwargs)


class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp", "updated", "image_link"]
	list_display_links = ["title"]
	list_filter = ["updated", "timestamp"]
	#list_editable = ["title"]
	search_fields = ["title", "content"]
	form = PostModelForm


admin.site.register(Post, PostModelAdmin)