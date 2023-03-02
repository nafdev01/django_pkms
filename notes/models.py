from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class CommonModel(models.Model):
    """
    Common abstract model for notes application course, topic,subtopic, and entry.
    """

    name = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        null=True,
        blank=True,
        editable=False,
    )
    updated = models.DateTimeField(default=timezone.now, editable=False)

    def get_absolute_url(self):
        return reverse(
            f"notes:{self._meta.verbose_name}_detail",
            args=[
                self.id,
                self.slug,
            ],
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Course(CommonModel):
    """
    Model for courses
    """

    class CertificationManager(models.Manager):
        def get_queryset(self):
            return (
                super()
                .get_queryset()
                .filter(course_type=Course.CourseType.CERTIFICATION)
            )

    class CourseWorkManager(models.Manager):
        def get_queryset(self):
            return (
                super().get_queryset().filter(course_type=Course.CourseType.COURSEWORK)
            )

    # choices for student year
    class CourseType(models.TextChoices):
        CERTIFICATION = "CT", "Certification"
        COURSEWORK = "CW", "Course Work"

    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE,
        null=True,
    )

    course_type = models.CharField(
        max_length=2,
        choices=CourseType.choices,
    )
    course_code = models.CharField(max_length=250, null=True, default="COSF")

    about = models.TextField()

    objects = models.Manager()  # The default manager.
    certifications = CertificationManager()  # Our custom manager.
    coursework_modules = CourseWorkManager()  # Our custom manager.

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.course_code = self.course_code.upper()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.course_code})"

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"
        ordering = ["course_code"]


class Topic(CommonModel):
    """
    model for course topic
    """

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        null=True,
    )
    number = models.PositiveIntegerField(null=True)
    overview = models.TextField(null=True, blank=True)

    @property
    def student(self):
        return {self.course.student}

    def __str__(self):
        return f"{self.number} {self.name} in {self.course.course_code}"

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"
        ordering = ["course", "number"]
        unique_together = ["course", "number"]


class SubTopic(CommonModel):
    """
    model for topic subtopic
    """

    topic = models.ForeignKey(
        "Topic",
        on_delete=models.CASCADE,
    )
    number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.topic.number}.{self.number} {self.name}"

    class Meta:
        verbose_name = "subtopic"
        verbose_name_plural = "subtopics"
        ordering = ["topic__number", "number"]
        unique_together = ["topic", "number"]


class Entry(CommonModel):
    """
    model for subtopic entry
    """

    subtopic = models.ForeignKey(
        "subtopic",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    content = models.TextField()
    revised = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"
        ordering = ["updated", "name"]
        unique_together = ["name", "subtopic"]
