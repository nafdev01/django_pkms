from django import template
from django.utils.safestring import mark_safe
import markdown
from glossary.models import *
from glossary.forms import *

register = template.Library()


@register.inclusion_tag("notes/includes/create_new_term.html")
def create_term_inline(entry):
    form = TermInlineForm()
    course = entry.subtopic.topic.course
    return {"course": course, "entry": entry, "form": form}
