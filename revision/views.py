# revision/views.py
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from notes.models import *
from revision.models import *
from revision.forms import ObjectiveForm

@login_required
def calendar(request):
    student = request.user
    objectives = Objective.objects.filter(course__student_id= student.id)
    courses = Course.objects.filter(student_id=student.id)
    

    template_path = 'revision/calendar.html'
    context = {'objectives': objectives, "courses": courses}
    return render(request, template_path, context)


# objective detail view
@login_required
def objective_detail(request, id, slug):
    student = request.user
    courses = Course.objects.filter(student_id=student.id)
    objective = get_object_or_404(Objective, id=id, slug=slug, course__student_id=student.id)
    other_objectives = Objective.objects.filter(course_id=objective.course.id, course__student_id=student.id).exclude(id=objective.id)
    
    template_path = "revision/objective_detail.html"
    context = {"student": student, "courses": courses,"objective": objective, "other_objectives": other_objectives
    }
    return render(request, template_path, context)


# create objective view 
@login_required
def create_objective(request, course_id):
    student = request.user
    course = get_object_or_404(Course,id=course_id, student_id=student.id)
    if request.method != 'POST':
        form = ObjectiveForm()
    else:
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            try:
                new_objective = form.save(commit=False)
                new_objective.course=course
                new_objective.save()
                return redirect(new_objective)
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    messages.error(request, f'An objective with that name already exists in this course.')
                else:
                    messages.error(request, 'There was an error creating the objective.')

    template_path = 'revision/create_objective_form.html'
    context = {'form': form}
    return render(request, template_path, context)


# update objective view
@login_required
def update_objective(request, objective_id, course_id):
    student = request.user
    course = get_object_or_404(Course,id=course_id, student_id=student.id)
    objective = get_object_or_404(Objective, id=objective_id, course__student_id=student.id)
    
    if request.method != 'POST':
        form = ObjectiveForm(instance=objective)
    else:
        form = ObjectiveForm(instance=objective, data=request.POST)
        if form.is_valid():
            try:
                updated_objective = form.save(commit=False)
                updated_objective.course = course
                return redirect(updated_objective)
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    messages.error(request, f'An objective with that name already exists in this course.')
                else:
                    messages.error(request, 'There was an error creating the objective.')

    template_path = 'revision/update_objective_form.html'
    context = {'form': form}
    return render(request, template_path, context)

# delete objective view
@login_required
def delete_objective(request, objective_id):
    student=request.user
    objective = Objective.objects.get(id=objective_id, course__student_id=student.id)
    objective_name = objective.name
    course = objective.course
    
    objective.delete()
    messages.success(request, f"The objective {objective_name} has been deleted successfully.")
    
    return redirect('revision:calendar')
