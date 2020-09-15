from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})


def new_list(request):
    list_ = List.objects.create()
    response = Item.objects.create(
        text=request.POST["new_item_text"], item_list=list_
    )
    return redirect("/lists/list-for-user/")
