from django.forms import ModelForm

from .models import BlogEntries


class BlogNew(ModelForm):
    class Meta:
        model = BlogEntries
        exclude = ('datetimeofentry','user')