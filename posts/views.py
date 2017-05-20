from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

def post_home(request):
	queryset_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(queryset_list, 3) #Show 25 posts per page
	
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"title": "Posts List",
		'object_list': queryset
	}

	return render(request, "post_list.html", context)

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Succesfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	elif form.errors:
		messages.error(request, "Not Succesfully Created")
	context = {
		"title": "Create New Note",
		"form": form
	}
	return render(request, "post_form.html", context)

def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	context = {
		"title": instance.title,
		"instance": instance
	}
	return render(request, "post_detail.html", context)

def post_update(request, id=None):
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Succesfully Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	elif form.errors:
		messages.error(request, "Not Succesfully Saved")

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form
	}
	return render(request, "post_form.html", context)


def post_delete(request, id=None):
	instance =get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Succesfully Deleted")
	return redirect("posts:home")

