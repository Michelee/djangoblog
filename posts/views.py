from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

def post_home(request):
	# if request.user.is_authenticated():
	# 	context = {
	# 		"title": "My Posts List"
	# 	}
	# else:
	# 	context = {
	# 		"title": "Posts List"
	# 	}
	queryset = Post.objects.all()
	context = {
 		"title": "Posts List",
 		'object_list': queryset
 	}

	return render(request, "index.html", context)

def post_create(request):
	return HttpResponse("<h1>Create</h1>")

def post_detail(request):
	instance = get_object_or_404(Post, id=2)
	context = {
		"title": instance.title,
		"instance": instance
	}
	return render(request, "detail.html", context)

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")
