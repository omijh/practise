# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect,get_object_or_404,reverse
from .models import user_info
# Create your views here.
def index(request):
	user_info_v = user_info.objects.all()[:10]
	context = {
		'user_info': user_info_v
	}
	return render(request,'index.html',context)

def addedit(request):
	# user_info_v = user_info.objects.all()
	print request.GET
	query = []
	if (request.method == 'POST'):
		# print request.get_full_path(),"\n\n\n"
		# olikh
		if 'slug' not in request.POST:
				if 'cancel' not in request.POST:
					first_name = request.POST['first_name']
					last_name = request.POST['last_name']
					email = request.POST['email']
					mobile = request.POST['mobile']
					dob = request.POST['dob']
					location = request.POST['location']
					ui = user_info(first_name=first_name, last_name=last_name,email=email,mobile=mobile,dob=dob,location=location)
					ui.save()
		else:
				if 'cancel' not in request.POST:
					update = user_info.objects.get(slug=request.POST['slug'])
					update.first_name = request.POST['first_name']
					update.last_name = request.POST['last_name']
					update.email = request.POST['email']
					update.mobile = request.POST['mobile']
					update.dob = request.POST['dob']
					update.location = request.POST['location']
					# ui = user_info(first_name=first_name, last_name=last_name,email=email,mobile=mobile,dob=dob,location=location)
					update.save()
		return redirect('/users')
	return render(request,'add.html')

def edit(request,slug):
	edit = get_object_or_404(user_info,slug=slug)
	print slug
	# if request.method == "POST":
	# 	form = PostForm(request.POST, instance=edit)
	# 	if form.is_valid():
	# 		edit = form.save(commit=False)
	# 		return redirect('UserInfo:index')
	# else:
	# 	form = PostForm(instance=edit)
	template = 'add.html'
	# edit = user_info.objects.get(id=id)
	context = {"slug": slug}
	return render(request, template, context)

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
#         redirect_url = reverse(article_save_success)
#         return redirect(redirect_url)

#     return render(request, template_name, {
#         'form': form
#     })