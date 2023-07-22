# revision/urls.py
from django.urls import path
from revision import views

app_name = "revision"

urlpatterns = [
    path("calendar", views.calendar, name="calendar"),
    path(
        "objective/course/<int:id>/<slug:slug>/",
        views.objective_list,
        name="objective_list",
    ),
    path(
        "objective/<int:id>/<slug:slug>/",
        views.objective_detail,
        name="objective_detail",
    ),
    path(
        "objective/create/",
        views.create_objective,
        name="create_objective",
    ),
    path(
        "subobjective/create/<int:objective_id>",
        views.create_subobjective,
        name="create_subobjective",
    ),
    path(
        "objective/update/<int:objective_id>/",
        views.update_objective,
        name="update_objective",
    ),
    path(
        "objective/delete/<int:objective_id>/",
        views.delete_objective,
        name="delete_objective",
    ),
    path(
        "subobjective/delete/<int:subobjective_id>/<path:object_path>/",
        views.delete_subobjective,
        name="delete_subobjective",
    ),
    path(
        "objective/mark_sub_complete/<int:subobjective_id>/<path:object_path>/",
        views.mark_sub_complete,
        name="mark_sub_complete",
    ),
    path(
        "objective/mark_sub_incomplete/<int:subobjective_id>/<path:object_path>/",
        views.mark_sub_incomplete,
        name="mark_sub_incomplete",
    ),
]
