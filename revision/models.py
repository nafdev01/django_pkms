# revision.models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from notes.models import Course, CommonModel, Topic


class Objective(CommonModel):
    number = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    duration = models.IntegerField(editable=False)
    complete = models.BooleanField(default=False)

    @property
    def has_subobjectives(self):
        if self.subobjective_set.all:
            return True
        else:
            return False

    @property
    def overdue(self):
        if not self.complete and timezone.now().date() > self.end_date:
            return True
        else:
            return False

    @property
    def in_progress(self):
        today = timezone.now().date()
        if self.start_date <= today and today <= self.end_date:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse(
            f"revision:{self._meta.verbose_name}_detail",
            args=[
                self.id,
                self.slug,
            ],
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days
        self.slug = slugify(self.name)
        super(Objective, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "objective"
        verbose_name_plural = "objectives"
        ordering = ["start_date", "end_date", "complete", "course"]
        unique_together = ["name", "course"]


class SubObjective(CommonModel):
    number = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE, null=True)
    duration = models.IntegerField(editable=False)
    complete = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def overdue(self):
        if not self.complete and timezone.now().date() > self.end_date:
            return True
        else:
            return False

    @property
    def in_progress(self):
        today = timezone.now().date()
        if self.start_date <= today and today <= self.end_date:
            return True
        else:
            return False

    def get_absolute_url(self):
        return self.objective.get_absolute_url()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days
        self.slug = slugify(self.name)
        super(SubObjective, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "sub objective"
        verbose_name_plural = "sub objectives"
        ordering = ["-complete", "number", "start_date", "end_date", "topic"]
        unique_together = ["name", "topic"]
