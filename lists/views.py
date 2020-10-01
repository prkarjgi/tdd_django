from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape
from django.core.exceptions import ValidationError
from lists.models import Item, List


def home_page(request):
    return render(request, "lists/home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == "POST":
        try:
            item = Item(item_list=list_, text=request.POST["new_item_text"])
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = escape("You cannot add an empty list item")
    return render(request, "lists/list.html", {"list": list_, "error": error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(
        text=request.POST["new_item_text"],
        item_list=list_
    )
    try:
        item.save()
        item.full_clean()
    except ValidationError as e:
        list_.delete()
        error = "You cannot add an empty list item"
        return render(
            request=request,
            template_name="lists/home.html",
            context={"error": error}
        )
    return redirect(list_)
