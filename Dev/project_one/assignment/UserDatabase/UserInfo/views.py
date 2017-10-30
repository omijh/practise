# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404,reverse
from .models import user_info
from .forms import UserForm
def index(request):
	user_info_v = user_info.objects.all()
	context = {
		'user_info': user_info_v
	}
	return render(request,'index.html',context)

def edit(request, id=None, template_name='add.html'):
    if id or ('id' in request.POST):
        ids = request.POST['id'] if 'id' in request.POST else ''
        ids = id if not ids else ids
        if ids and ids != 'None':
            instance = get_object_or_404(user_info, pk=ids)
        else:
            instance = user_info()
    else:
        instance = user_info()
    form = UserForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        redirect_url = reverse('index')
        return redirect(redirect_url)

    return render(request, template_name, {
        'form': form,
        'id':id,
    })

# def add(request):
# 	form = UserForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		return redirect('/')
# 	context = {
# 		"form": form,
# 	}
# 	return render(request, "add.html",context)
# def edit(request, id=None):
#     recipe = get_object_or_404(user_info, pk=id)
#     if request.method == "POST":
#         form = UserForm(request.POST, instance=recipe)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             # recipe.user = request.user
#             # recipe.save()
#             return redirect('index', pk=recipe.pk)
#     else:
#         form = UserForm(instance=recipe)
#     return render(request, 'add.html', {'form': form, 'recipe':recipe})
# def edit(request,id=None):
# 	if id:
# 		print id
# 		instance = get_object_or_404(user_info,id=id)
# 		form = UserForm(request.POST or None, instance=instance)
# 		# else:
# 		# 	form = UserForm(request.POST or None)
# 		print form.is_valid()
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.save()
# 			return redirect('/')

# 		context = {
# 			"first_name": instance.first_name,
# 			"last_name": instance.last_name,
# 			"email": instance.email,
# 			"mobile": instance.mobile,
# 			"dob": instance.dob,
# 			"location":instance.location,
# 			"form": form,
# 		}
# 	else:
# 		form = UserForm(request.POST or None)
# 		print form.is_valid(),"new"
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.save()
# 			return redirect('/')
# 		context = {
# 			"form": form,
# 		}
# 	return render(request, "add.html",context)


# def addedit(request):
# 	# user_info_v = user_info.objects.all()
# 	print request.GET
# 	query = []
# 	if (request.method == 'POST'):
# 		# print request.get_full_path(),"\n\n\n"
# 		# olikh
# 		if 'slug' not in request.POST:
# 				if 'cancel' not in request.POST:
# 					first_name = request.POST['first_name']
# 					last_name = request.POST['last_name']
# 					email = request.POST['email']
# 					mobile = request.POST['mobile']
# 					dob = request.POST['dob']
# 					location = request.POST['location']
# 					ui = user_info(first_name=first_name, last_name=last_name,email=email,mobile=mobile,dob=dob,location=location)
# 					ui.save()
# 		else:
# 				if 'cancel' not in request.POST:
# 					update = user_info.objects.get(slug=request.POST['slug'])
# 					update.first_name = request.POST['first_name']
# 					update.last_name = request.POST['last_name']
# 					update.email = request.POST['email']
# 					update.mobile = request.POST['mobile']
# 					update.dob = request.POST['dob']
# 					update.location = request.POST['location']
# 					# ui = user_info(first_name=first_name, last_name=last_name,email=email,mobile=mobile,dob=dob,location=location)
# 					update.save()
# 		return redirect('/users')
# 	return render(request,'add.html')



# def edit(request,slug):
# 	edit = get_object_or_404(user_info,slug=slug)
# 	print slug
# 	# if request.method == "POST":
# 	# 	form = PostForm(request.POST, instance=edit)
# 	# 	if form.is_valid():
# 	# 		edit = form.save(commit=False)
# 	# 		return redirect('UserInfo:index')
# 	# else:
# 	# 	form = PostForm(instance=edit)
# 	template = 'add.html'
# 	# edit = user_info.objects.get(id=id)
# 	context = {"slug": slug}
# 	return render(request, template, context)

# def update(request,id):
# 	update = user_info.objects.get(id=id)
# 	update.first_name = request.POST['first_name']
# 	update.last_name = request.POST['last_name']
# 	update.email = request.POST['email']
# 	update.mobile = request.POST['mobile']
# 	update.dob = request.POST['dob']
# 	update.location = request.POST['location']
# 	update.save()
# 	return redirect('/')
# def edit(request, id=None, template_name='add.html'):
#     if id:
#         article = get_object_or_404(user_info, pk=id)
#         if article.author != request.user:
#             return HttpResponseForbidden()
#     else:
#         article = Article(author=request.user)

#     form = ArticleForm(request.POST or None, instance=article)
#     if request.POST and form.is_valid():
#         form.save()

#         # Save was successful, so redirect to another page
#         redirect_url = reverse('/')
#         return redirect(redirect_url)

#     return render(request, template_name, {
#         'form': form
#     })