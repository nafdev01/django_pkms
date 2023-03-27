# glossary/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from notes.models import *
from glossary.models import *
from glossary.forms import *


# terms list
@login_required
def term_list(request, course_id=None, slug=None, first_letter=None):
    student = request.user
    terms = Term.objects.filter(course__student_id=student.id)
    courses = sorted(set([term.course for term in terms]))
    first_letters = sorted(set([term.name[0].upper() for term in terms]))

    context = {"courses": courses, "first_letters": first_letters}

    if course_id:
        course = get_object_or_404(Course, id=course_id, slug=slug)
        terms = Term.objects.filter(course_id=course.id, course__student_id=student.id)
        messages.info(request, f"Now showing terms for course  '{course.name}'.")
        context.update({"terms": terms, "course": course})
    elif first_letter:
        terms = terms.filter(name__startswith=first_letter)
        messages.info(request, f"Now showing terms that start with '{first_letter}'.")
        context.update({"terms": terms, "first_letter": first_letter})
    else:
        messages.info(request, f"Now showing all terms.")
        context.update({"terms": terms})

    template_path = "glossary/term_list.html"
    return render(request, template_path, context)


"""
create views
"""


@login_required
def create_term(request):
    student = request.user
    if request.method != "POST":
        form = TermForm(student=student)
    else:
        form = TermForm(student=student, data=request.POST)
        if form.is_valid():
            try:
                new_term = form.save(commit=False)
                new_term.save()
                return redirect(new_term)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    messages.error(request, f"A term with that title already exists")
                else:
                    messages.error(request, "There was an error creating the term.")

    template_path = "glossary/term_create_form.html"
    context = {"form": form}
    return render(request, template_path, context)


@login_required
def create_term_inline(request, entry_id, course_id):
    student = request.user
    entry = get_object_or_404(
        Entry, id=entry_id, subtopic__topic__course__student=student
    )
    course = get_object_or_404(Course, id=course_id, student=student)
    if request.method != "POST":
        form = TermInlineForm()
    else:
        form = TermInlineForm(data=request.POST)
        if form.is_valid():
            try:
                new_term = form.save(commit=False)
                new_term.course = course
                new_term.save()
                messages.success(
                    request,
                    f"Successfully created term '{new_term}' in {course.course_code}",
                )
                return redirect(entry)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    messages.error(request, f"A term with that title already exists")
                    return redirect(entry)
                else:
                    messages.error(request, "There was an error creating the term.")
                    return redirect(entry)


"""
update views
"""


@login_required
def update_term(request, term_id):
    student = request.user
    term = get_object_or_404(Term, id=term_id, course__student_id=student.id)
    if request.method != "POST":
        form = TermForm(student=student, instance=term)
    else:
        form = TermForm(student=student, instance=term, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(term)

    template_path = "glossary/term_update_form.html"
    context = {"form": form, "term": term}
    return render(request, template_path, context)


"""
delete views
"""


@login_required
def delete_term(request, term_id):
    student = request.user
    term = Term.objects.get(id=term_id, course__student_id=student.id)
    term_name = term.name

    term.delete()
    messages.success(request, f"The term {term_name} has been deleted successfully.")

    return redirect("glossary:term_list")
