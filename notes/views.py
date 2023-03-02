from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import markdown
from django.contrib import messages
from django.db import IntegrityError
from notes.models import *
from notes.forms import *
from glossary.models import *
from revision.models import *


@login_required
def dashboard(request):
    student = request.user
    courses = Course.objects.filter(student_id=student.id).order_by("updated")
    latest_entries = Entry.objects.filter(
        subtopic__topic__course__student_id=student.id
    ).order_by("-updated")[:5]

    today = timezone.now().date()
    objectives = Objective.objects.filter(
        end_date__gte=today, start_date__lte=today, complete=False
    )

    template_path = "notes/dashboard.html"
    context = {
        "student": student,
        "latest_entries": latest_entries,
        "student": student,
        "courses": courses,
        "objectives": objectives,
    }
    return render(request, template_path, context)


# course detail
@login_required
def course_detail(request, id, slug):
    student = request.user
    course = get_object_or_404(Course, id=id, slug=slug, student_id=student.id)
    topics = course.topic_set.filter(course__student_id=student.id, course_id=course.id)

    template_path = "notes/detail/course_detail.html"
    context = {
        "student": student,
        "course": course,
        "topics": topics,
    }
    return render(request, template_path, context)


@login_required
def topic_detail(request, id, slug):
    student = request.user
    topic = get_object_or_404(Topic, id=id, slug=slug, course__student_id=student.id)
    other_topics = Topic.objects.filter(
        course_id=topic.course.id, course__student_id=student.id
    ).exclude(id=topic.id)
    subtopics = topic.subtopic_set.filter(topic__course__student_id=student.id)

    template_path = "notes/detail/topic_detail.html"
    context = {
        "student": student,
        "topic": topic,
        "subtopics": subtopics,
        "other_topics": other_topics,
    }
    return render(request, template_path, context)


@login_required
def subtopic_detail(request, id, slug):
    student = request.user
    subtopic = get_object_or_404(
        SubTopic, id=id, slug=slug, topic__course__student_id=student.id
    )
    other_subtopics = SubTopic.objects.filter(
        topic_id=subtopic.topic.id, topic__course__student_id=student.id
    ).exclude(id=subtopic.id)
    entries = subtopic.entry_set.filter(subtopic__topic__course__student_id=student.id)

    template_path = "notes/detail/subtopic_detail.html"
    context = {
        "student": student,
        "subtopic": subtopic,
        "other_subtopics": other_subtopics,
        "entries": entries,
    }
    return render(request, template_path, context)


@login_required
def entry_detail(request, id, slug):
    student = request.user
    entry = get_object_or_404(
        Entry, id=id, slug=slug, subtopic__topic__course__student_id=student.id
    )
    other_entries = Entry.objects.filter(
        subtopic_id=entry.subtopic.id, subtopic__topic__course__student_id=student.id
    ).exclude(id=entry.id)

    template_path = "notes/detail/entry_detail.html"
    context = {"student": student, "entry": entry, "other_entries": other_entries}
    return render(request, template_path, context)


"""
create views
"""


@login_required
def create_course(request):
    student = request.user
    if request.method != "POST":
        form = CourseForm()
    else:
        form = CourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.student = student
            new_course.save()
            return redirect(new_course)

    template_path = "notes/create/course_create_form.html"
    context = {"form": form}
    return render(request, template_path, context)


@login_required
def create_topic(request, course_id):
    student = request.user
    course = get_object_or_404(Course, id=course_id, student_id=student.id)
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            try:
                new_topic = form.save(commit=False)
                new_topic.course = course
                new_topic.save()
                return redirect(new_topic)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    messages.error(
                        request,
                        f'A topic with that number already exists in this course "{course.course_code}".',
                    )
                else:
                    messages.error(request, "There was an error creating the topic.")

    template_path = "notes/create/topic_create_form.html"
    context = {"form": form}
    return render(request, template_path, context)


@login_required
def create_subtopic(request, topic_id):
    student = request.user
    topic = get_object_or_404(Topic, id=topic_id, course__student_id=student.id)
    if request.method != "POST":
        form = SubTopicForm()
    else:
        form = SubTopicForm(data=request.POST)
        if form.is_valid():
            try:
                new_subtopic = form.save(commit=False)
                new_subtopic.topic = topic
                new_subtopic.save()
                return redirect(new_subtopic)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    messages.error(
                        request,
                        f'A subtopic with that number already exists in this topic "{topic}".',
                    )
                else:
                    messages.error(request, "There was an error creating the subtopic.")

    template_path = "notes/create/subtopic_create_form.html"
    context = {"form": form}
    return render(request, template_path, context)


@login_required
def create_entry(request, subtopic_id):
    student = request.user
    subtopic = get_object_or_404(
        SubTopic, id=subtopic_id, topic__course__student_id=student.id
    )
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            try:
                new_entry = form.save(commit=False)
                new_entry.subtopic = subtopic
                new_entry.save()
                return redirect(new_entry)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    messages.error(
                        request,
                        f'An entry with that title already exists in subtopic "{subtopic}".',
                    )
                else:
                    messages.error(request, "There was an error creating the entry.")

    template_path = "notes/create/entry_create_form.html"
    context = {"form": form}
    return render(request, template_path, context)


"""
update views
"""


@login_required
def update_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method != "POST":
        form = CourseForm(instance=course)
    else:
        form = CourseForm(instance=course, data=request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect(course)

    template_path = "notes/update/course_update_form.html"
    context = {"form": form, "course": course}
    return render(request, template_path, context)


@login_required
def update_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(topic)

    template_path = "notes/update/topic_update_form.html"
    context = {"form": form, "topic": topic}
    return render(request, template_path, context)


@login_required
def update_subtopic(request, subtopic_id):
    subtopic = SubTopic.objects.get(id=subtopic_id)
    if request.method != "POST":
        form = SubTopicForm(instance=subtopic)
    else:
        form = SubTopicForm(instance=subtopic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(subtopic)

    template_path = "notes/update/subtopic_update_form.html"
    context = {"form": form, "subtopic": subtopic}
    return render(request, template_path, context)


@login_required
def update_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(entry)

    template_path = "notes/update/entry_update_form.html"
    context = {"form": form, "entry": entry}
    return render(request, template_path, context)


"""
delete views
"""


# delete course view
@login_required
def delete_course(request, course_id):
    student = request.user
    course = Course.objects.get(id=course_id, student_id=student.id)
    course_name = course.name

    course.delete()
    messages.success(
        request, f"The course {course_name} has been deleted successfully."
    )

    return redirect("notes:dashboard")


# delete topic view
@login_required
def delete_topic(request, topic_id):
    student = request.user
    topic = Topic.objects.get(id=topic_id, course__student_id=student.id)
    topic_name = topic.name
    course = topic.course

    topic.delete()
    messages.success(request, f"The topic {topic_name} has been deleted successfully.")

    return redirect(course)


# delete subtopic view
@login_required
def delete_subtopic(request, subtopic_id):
    student = request.user
    subtopic = SubTopic.objects.get(
        id=subtopic_id, topic__course__student_id=student.id
    )
    subtopic_name = subtopic.name
    topic = subtopic.topic

    subtopic.delete()
    messages.success(
        request, f"The subtopic {subtopic_name} has been deleted successfully."
    )

    return redirect(topic)


# delete entry view
@login_required
def delete_entry(request, entry_id):
    student = request.user
    entry = Entry.objects.get(
        id=entry_id, subtopic__topic__course__student_id=student.id
    )
    entry_name = entry.name
    subtopic = entry.subtopic

    entry.delete()
    messages.success(request, f"The entry {entry_name} has been deleted successfully.")

    return redirect(subtopic)


"""
Additional views
"""


# search for entries, subtopics, topics and courses
def search(request):
    student = request.user
    query = request.GET.get("q")
    if query:
        objectives = Objective.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            course__student_id=student.id,
        )
        terms = Term.objects.filter(
            Q(name__icontains=query) | Q(definition__icontains=query),
            course__student_id=student.id,
        )
        entries = Entry.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query),
            subtopic__topic__course__student_id=student.id,
        )
        subtopics = SubTopic.objects.filter(
            Q(name__icontains=query), topic__course__student_id=student.id
        )
        topics = Topic.objects.filter(
            Q(name__icontains=query) | Q(overview__icontains=query),
            course__student_id=student.id,
        )
        courses = Course.objects.filter(
            Q(name__icontains=query)
            | Q(course_type__icontains=query)
            | Q(course_code__icontains=query)
            | Q(about__icontains=query),
            student_id=student.id,
        )
    else:
        objectives = Objective.objects.filter(course__student_id=student.id)
        terms = Term.objects.filter(course__student_id=student.id)
        entries = Entry.objects.filter(subtopic__topic__course__student_id=student.id)
        subtopics = SubTopic.objects.filter(topic__course__student_id=student.id)
        topics = Topic.objects.filter(course__student_id=student.id)
        courses = Course.objects.filter(student_id=student.id)

    template_path = "notes/search.html"
    context = {
        "terms": terms,
        "entries": entries,
        "subtopics": subtopics,
        "topics": topics,
        "courses": courses,
        "objectives": objectives,
    }
    return render(request, template_path, context)


# send entry by email
def entry_share(request, entry_id):
    student = request.user
    # Retrieve entry by id
    entry = get_object_or_404(
        Entry, id=entry_id, subtopic__topic__course__student_id=student.id
    )
    entry_url = request.build_absolute_uri(entry.get_absolute_url())
    subject = f"{student.get_full_name()} has sent you notes on {entry.subtopic}"
    sender = settings.EMAIL_HOST_USER
    recipient = request.GET.get("recipient")
    message = get_template("notes/includes/entry_email_template.html").render(
        {"entry": entry, "entry_url": entry_url}
    )
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=sender,
        to=[recipient],
        reply_to=[sender],
    )
    mail.content_subtype = "html"
    if mail.send():
        messages.success(
            request, f"The entry '{entry}'was successfully shared with '{recipient}'"
        )
    else:
        messages.error(
            request, f"The entry '{entry}' could not be shared with '{recipient}'"
        )

    return redirect(entry)
