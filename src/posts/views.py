# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm


# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully Created")

        # return HttpResponseRedirect(instance.get_absolute_url())
        # return HttpResponseRedirect(reverse("posts:detail", kwargs={"id":instance.id}))
        # return HttpResponseRedirect(reverse("posts:detail", kwargs={"id": instance.id}))
        return redirect(reverse("posts:detail", kwargs={"id": instance.id}))
    else:
        messages.error(request, "Not Successfully Created")
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all() # .order_by("-timestamp")

    paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page

    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None , instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')

        # message success
        # return HttpResponseRedirect(instance.get_absolute_url())
        return HttpResponseRedirect(reverse("posts:detail", kwargs={"slug": instance.slug}))

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
