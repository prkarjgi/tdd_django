from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "You cannot add an empty list item"


class ItemForm(forms.ModelForm):

    class Meta(object):
        model = Item
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "placeholder": "Enter a new item",
                    "class": "form-control input-lg",
                }
            )
        }
        error_messages = {
            "text": {
                "required": EMPTY_ITEM_ERROR
            }
        }
