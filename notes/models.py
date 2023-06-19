from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


def reference_book_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.course.student.username}/reference_books/{instance.course.course_code}/{instance.title}"


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

    class OtherCourseManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(course_type=Course.CourseType.OTHER)

    # choices for student year
    class CourseType(models.TextChoices):
        CERTIFICATION = "CT", "Certification"
        COURSEWORK = "CW", "Course Work"
        OTHER = "OT", "Other"

    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE,
        null=True,
    )

    course_type = models.CharField(
        max_length=2,
        choices=CourseType.choices,
    )
    course_code = models.CharField(max_length=250, null=True, default="CODE")

    about = models.TextField()

    objects = models.Manager()  # The default manager.
    certifications = CertificationManager()  # Our custom manager.
    coursework_modules = CourseWorkManager()  # Our custom manager.
    others = OtherCourseManager()  # Our custom manager.

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.course_code = self.course_code.upper()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.course_code})"

    @property
    def other_courses(self):
        courses = Course.objects.filter(student_id=self.student.id).exclude(id=self.id)
        return courses

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

    @property
    def other_topics(self):
        topics = Topic.objects.filter(
            course__student_id=self.course.student.id, course_id=self.course.id
        ).exclude(id=self.id)
        return topics

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

    @property
    def other_subtopics(self):
        other_subtopics = SubTopic.objects.filter(
            topic_id=self.topic.id,
            topic__course__student_id=self.topic.course.student.id,
        ).exclude(id=self.id)
        return other_subtopics

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

    @property
    def other_entries(self):
        other_entries = Entry.objects.filter(
            subtopic_id=self.subtopic.id,
            subtopic__topic__course__student_id=self.subtopic.topic.course.student.id,
        ).exclude(id=self.id)
        return other_entries

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"
        ordering = ["updated", "name"]
        unique_together = ["name", "subtopic"]


class ReferenceBook(models.Model):
    """
    model for course reference books
    """

    title = models.CharField()
    slug = models.SlugField(
        max_length=250,
        null=True,
        blank=True,
        editable=False,
    )

    author = models.CharField()
    course = models.ForeignKey(
        "course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    year_of_publication = models.IntegerField()
    edition = models.CharField()
    file = models.FileField(upload_to=reference_book_path, blank=True, null=True)

    @property
    def other_entries(self):
        other_entries = Entry.objects.filter(
            subtopic_id=self.subtopic.id,
            subtopic__topic__course__student_id=self.subtopic.topic.course.student.id,
        ).exclude(id=self.id)
        return other_entries

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "reference book"
        verbose_name_plural = "reference books"
        ordering = ["course", "title"]
        unique_together = ["title", "course"]
