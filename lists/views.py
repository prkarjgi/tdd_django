from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(
            item_list=list_, text=request.POST["new_item_text"]
        )
        return redirect(f"/lists/{list_.id}/")
    return render(request, "list.html", {"list": list_})


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
            template_name="home.html",
            context={"error": error}
        )
    return redirect(f"/lists/{list_.id}/")
