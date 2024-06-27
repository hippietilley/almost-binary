from django.conf import settings
from django.db import models
from django.utils import timezone

from markdown import markdown


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    markdown_content = models.TextField()
    rendered_content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def _render_text(self):
        self.rendered_content = markdown(markdown_content)

    def publish(self):
        self._render_text()
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"pk": self.pk})