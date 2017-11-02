# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import info_sys
from .forms import Info_sys
from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib  import messages

def index(request):
	info_sys_v = info_sys.objects.all()
	context = {
		'info_sys': info_sys_v
	}
	return render(request,'index.html',context)

def edit(request, id=None, template_name='add.html'):
    if id or ('id' in request.POST):
        ids = request.POST['id'] if 'id' in request.POST else ''
        ids = id if not ids else ids
        if ids and ids != 'None':
            instance = get_object_or_404(info_sys, pk=ids)
        else:
            instance = info_sys()
    else:
        instance = info_sys()
    form = Info_sys(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        redirect_url = reverse('index')
        return redirect(redirect_url)

    return render(request, template_name, {
        'form': form,
        'id':id,
    })

def delete(request, id=None):
    if id:
        info_sys.objects.filter(pk=id).update(isActive=False)
        messages.success(request, "Successfully deleted")
    return redirect("index")

