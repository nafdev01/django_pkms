from django import template
from django.utils.safestring import mark_safe
import markdown
from notes.models import *

register = template.Library()

@register.inclusion_tag('notes/includes/go_to.html')
def go_to(request):
    request = request
    courses = Course.objects.filter(student_id=request.user.id)
    return {"courses": courses , "request": request}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))