from django.db import models

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from markdown import markdown


class CV(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    skills = models.JSONField(default=dict, blank=True, help_text="{type: [skill1, skill2]}")
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    website = models.CharField(max_length=256, blank=True, null=True)
    tag_line = models.TextField(blank=True, null=True)
    professional_interests = ArrayField(
        models.CharField(max_length=256, blank=True),
        blank=True,
        default=list,
    )
    personal_interests = ArrayField(
        models.CharField(max_length=256, blank=True),
        blank=True,
        default=list,
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Experience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    skills = models.JSONField(default=dict, blank=True, help_text="{type: [skill1, skill2]}")
    company = models.CharField(max_length=256, blank=True, null=True)
    job_description = models.TextField()
    job_title = models.CharField(max_length=256, blank=True, null=True)
    job_location = models.CharField(max_length=256, blank=True, null=True)
    job_skills = models.JSONField(default=dict, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(blank=True, null=True)

class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=256, blank=True, null=True)
    degree = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(blank=True, null=True)

class CommunityInvolvement(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(blank=True, null=True)

class About(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    markdown_content = models.TextField()
    rendered_content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def _render_text(self):
        self.rendered_content = markdown(markdown_content)

    def publish(self):
        self._render_text()
        self.published_date = timezone.now()
        self.save()