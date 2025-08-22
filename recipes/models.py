from django.conf import settings
from django.db import models
from django.utils import timezone

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="recipes/images")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField()  # 1–5
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"{self.user.username} -> {self.recipe.name}: {self.score}"
