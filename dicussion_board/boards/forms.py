from django import forms
from .models import *


# =================================================================
class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "what is on your mind?"}
        ),
        max_length=5000,
        help_text="The max length od the text is 5000",
        required=True,
    )

    class Meta:
        model = Topic  # model
        fields = ["subject", "message"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # model
        fields = [
            "message",
        ]
