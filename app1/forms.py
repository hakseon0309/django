from django.forms import ModelForm
from .models import Post, MrtMemoMaker


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
