from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from . import models
from . import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.views.generic import ListView


# @login_required
def all_materials(request):
    # material_list = models.Material.objects.all()
    material_list = models.Material.theory.all()
    return render(request,
                  'materials/all_materials.html',
                  {"materials": material_list})


# class MaterialListView(LoginRequiredMixin, ListView):
#     queryset = models.Material.objects.all()
#     context_object_name = 'materials'
#     template_name = 'materials/all_materials.html'


def material_details(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)

    new_comment = None
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.material = material
            new_comment.save()
            return redirect(material)
    else:
        comment_form = forms.CommentForm()
    return render(request,
                  'materials/detail.html',
                  {'material': material,
                   'form': comment_form,
                   'new_comment': new_comment, })


def share_material(request, material_id):
    material = get_object_or_404(models.Material,
                                 id=material_id)
    sent = False
    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            material_uri = request.build_absolute_uri(
                material.get_absolute_url(),
            )
            subject = "{} ({}) recommends you {}".format(
                cd['name'],
                cd['my_email'],
                material.title,
            )
            body = "{title} at {uri}\n\n {name} recommends you with comment:\n\n{comment}".format(
                title=material.title,
                uri=material_uri,
                name=cd['name'],
                comment=cd['comment'],
            )
            send_mail(subject, body, 'admin@mysite.com', [cd['to_email'], ])
            sent = True
    else:
        form = forms.EmailMaterialForm()
    return render(request,
                  'materials/share.html',
                  {'material': material, 'form': form, 'sent':sent})


def create_form(request):
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()
            return render(request,
                          'materials/detail.html',
                          {'material': new_material})
    else:
        material_form = forms.MaterialForm()
    return render(request,
                  "materials/create.html",
                  {'form': material_form})


def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Auth successfull')
                else:
                    HttpResponse('inactive user')
            else:
                return HttpResponse('BAD Credentials')
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})
