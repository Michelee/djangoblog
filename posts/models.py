from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.html import format_html

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	title = models.CharField(max_length=150)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location,
		null=True, 
		blank=True, 
		width_field="width_field", 
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	referer = models.TextField()

	def __unicode__(self):
		return self.title
	
	def __str__(self):
		return self.title	

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id": self.id})
		#return "/posts/%s/" %(self.id)

	def image_link(self):
		if self.image:
			return '<a target="_blank" href="%s">%s</a>' % (self.image.url, self.image)
		
	
	image_link.allow_tags = True

	class Meta:
		ordering = ["-updated", "-timestamp"]


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	slug = slugify(instance.title)
	exists = Post.objects.filter(slug=slug).exists()
	if exists:
		slug = "%s-%s" %(slug, instance.id)
	instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)

