from django.contrib import admin
from .models import User
from recipes.models import Recipe, Rating


admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Rating)
