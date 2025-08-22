from django.db.models import Avg, Count
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle

from accounts.permissions import IsSeller, IsCustomer
from .models import Recipe, Rating
from .serializers import RecipeSerializer, RatingSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle, ScopedRateThrottle]

    def get_queryset(self):
        return Recipe.objects.select_related("author").annotate(
            avg_rating=Avg("ratings__score"),
            rating_count=Count("ratings")
        )

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsSeller()]
        return [permissions.IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author_id != request.user.id:
            return Response({"detail": "Only the owner can delete this recipe."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class RatingViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    throttle_classes = [UserRateThrottle, ScopedRateThrottle]

    def get_queryset(self):
        qs = Rating.objects.select_related("recipe", "user")
        recipe_id = self.request.query_params.get("recipe")
        if recipe_id:
            qs = qs.filter(recipe_id=recipe_id)
        return qs
