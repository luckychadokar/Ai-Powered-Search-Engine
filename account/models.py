from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecentSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    query = models.CharField(max_length=255, verbose_name="Search Query")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Search Time")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Recent Search"
        verbose_name_plural = "Recent Searches"

    def __str__(self):
        return f"{self.user.username} - {self.query}"


class GenerationHistory(models.Model):
    prompt = models.TextField(verbose_name="Prompt")
    negative_prompt = models.TextField(blank=True, null=True, verbose_name="Negative Prompt")
    width = models.IntegerField(verbose_name="Image Width")
    height = models.IntegerField(verbose_name="Image Height")
    images = models.JSONField(verbose_name="Generated Images")  # base64 or URLs
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Generated At")

    # Optional: If you later store generated images as files
    # image_file = models.ImageField(upload_to='generated_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Image Generation History"
        verbose_name_plural = "Image Generation History"

    def __str__(self):
        return f"Generated at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
