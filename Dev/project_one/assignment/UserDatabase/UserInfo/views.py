# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib  import messages
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

def delete(request, id=None):
    instance = get_object_or_404(user_info, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("index")

