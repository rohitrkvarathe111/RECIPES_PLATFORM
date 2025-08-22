from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Recipe, Rating
from .tasks import resize_recipe_image


class RecipeSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ["id", "name", "description", "image", "author", "author_username", "created_at", "updated_at", "avg_rating", "rating_count"]
        read_only_fields = ["author", "created_at", "updated_at", "avg_rating", "rating_count", "author_username"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        recipe = super().create(validated_data)
        resize_recipe_image.delay(recipe.id)     
        return recipe

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "recipe", "user", "score", "created_at"]
        read_only_fields = ["user", "created_at"]

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        recipe = attrs.get("recipe")

        # 1. Prevent sellers from rating their own recipe
        if recipe and recipe.author_id == user.id:
            raise serializers.ValidationError("Sellers cannot rate their own recipes.")

        # 2. Prevent duplicate ratings by same user
        if Rating.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("You have already rated this recipe.")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
