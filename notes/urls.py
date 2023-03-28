# notes/urls.py
from django.urls import path
from notes import views

app_name = "notes"

urlpatterns = [
    #
    # LIST URLS
    #
    path("dashboard", views.dashboard, name="dashboard"),
    #
    # detail views
    #
    path('course/<int:id>/<slug:slug>/', views.course_detail, name='course_detail'),
    path('topic/<int:id>/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('subtopic/<int:id>/<slug:slug>/', views.subtopic_detail, name='subtopic_detail'),
    path('entry/<int:id>/<slug:slug>/', views.entry_detail, name='entry_detail'),
    #
    # create views
    #
    path("course/create/", views.create_course, name="create_course"),
    path("topic/create/<int:course_id>", views.create_topic, name="create_topic"),
    path("subtopic/create/<int:topic_id>", views.create_subtopic, name="create_subtopic"),
    path("entry/create/<int:subtopic_id>", views.create_entry, name="create_entry"),
    #
    # update views
    #
    path("course/update/<int:course_id>", views.update_course, name="update_course"),
    path("topic/update/<int:topic_id>", views.update_topic, name="update_topic"),
    path("subtopic/update/<int:subtopic_id>", views.update_subtopic, name="update_subtopic"),
    path("entry/update/<int:entry_id>", views.update_entry, name="update_entry"),
    #
    # update views
    #
    path("course/delete/<int:course_id>/", views.delete_course, name="delete_course"),
    path("topic/delete/<int:topic_id>/", views.delete_topic, name="delete_topic"),
    path("subtopic/delete/<int:subtopic_id>/", views.delete_subtopic, name="delete_subtopic"),
    path("entry/delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    #
    # additional urls
    #
    path('search/', views.search, name='search'),
    path("entry/share/<int:entry_id>/", views.entry_share, name="entry_share"),
]
