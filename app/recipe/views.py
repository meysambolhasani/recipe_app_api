from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        assigned_only=bool(
            int(self.request.query_params.get('assigned_only',0)) # 0 is a default value for assigned_only .note int() cannot convert None to integer
        )
        queryset=self.queryset
        if assigned_only:
            queryset=queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage tag in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredient in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe in the database"""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)



    def get_queryset(self):
        """ Return recipe for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return approciate serializer class"""

        if self.action == 'retrieve':
            return RecipeDetailSerializer

        return self.serializer_class