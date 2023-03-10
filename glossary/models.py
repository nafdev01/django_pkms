# glossary/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from notes.models import Course, CommonModel


class Term(CommonModel):
    """
    model for important terms in courses
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    definition = models.TextField()
    
    @property
    def student(self):
        return {self.course.student}

    def get_absolute_url(self):
        return reverse(
            f"glossary:terms_by_course",
            args=[
                self.course.id,
                self.course.slug,
            ],
        )
        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
    	ordering = ['course','name']
