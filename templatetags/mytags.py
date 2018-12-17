from datetime import datetime

from django import template

from ..models import BlogEntries

register = template.Library()

@register.simple_tag
def current_time():
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    return formatedDate

@register.inclusion_tag('fetch_blog.html')
def fetch_blogentries():
   queryset = BlogEntries.objects.all()
   context = {
       "entries": queryset
   }
   return context
