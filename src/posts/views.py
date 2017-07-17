# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Post
from .forms import PostForm


# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully Created")

        # return HttpResponseRedirect(instance.get_absolute_url())
        # return HttpResponseRedirect(reverse("posts:detail", kwargs={"id":instance.id}))
        return HttpResponseRedirect(reverse("posts:detail", kwargs={"id": instance.id}))
    else:
        messages.error(request, "Not Successfully Created")
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }

    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()

    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request, "post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')

        # message success
        # return HttpResponseRedirect(instance.get_absolute_url())
        return HttpResponseRedirect(reverse("posts:detail", kwargs={"id": instance.id}))

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
