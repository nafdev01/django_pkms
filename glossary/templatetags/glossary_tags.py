from django import template
from django.utils.safestring import mark_safe
import markdown
from glossary.models import *
from glossary.forms import *

register = template.Library()


@register.inclusion_tag("notes/includes/create_new_term.html")
def create_term_inline(topic):
    form = TermInlineForm()
    course = topic.course
    return {"course": course, "topic": topic, "form": form}
