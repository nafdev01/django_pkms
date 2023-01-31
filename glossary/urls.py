# glossary/urls.py
from django.urls import path
from glossary import views

app_name = "glossary"

urlpatterns = [
    #
    # LIST URLS
    #
    path("", views.term_list, name="term_list"),
    path('<int:course_id>/<slug:slug>/', views.term_list, name='terms_by_course'),
    #
    # create views
    #
    path("term/create/", views.create_term, name="create_term"),
    #
    # update views
    #
    path("term/update/<int:term_id>", views.update_term, name="update_term"),
    #
    # update views
    #
    path("term/delete/<int:term_id>/", views.delete_term, name="delete_term"),
]
