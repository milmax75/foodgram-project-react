from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ingredients, Recipe, Tag, ShopList, Favourites
from .serializers import (
    IngredientsSerializer,
    TagSerializer,
    FavouritesSerializer,
    ShopListSerializer,
    CreateUpdateRecipeSerializer,
    IngredientInRecipeSerializer
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientsFilter

#from .permissions import AllowAny


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [IngredientsFilter]
    search_fields = ['^name']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavouritesViewSet(viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer


class ShopListViewSet(viewsets.ModelViewSet):
    queryset = ShopList.objects.all()
    serializer_class = ShopListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = CreateUpdateRecipeSerializer

    '''def get_queryset(self):
        qs = Tag.objects.all().id
        return qs'''

    '''def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return CreateRecipeSerializer'''
        # return ...

    def download_shopping_cart(self, request):
        '''Download shoplist file in pdf format'''
        shoplist = {}
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shoplist_recipe__user=request.user
            )
            .values('ingredient__name', 'ingredient__units')
            .order_by('ingredient__name')
            .annotate(total=Sum('quantity'))
        )
        output = 'The list of goods for your recipes. \n'
        output += '\n'.join(
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}   '
                f'{ingredient["ingredient__units"]}'
                for ingredient in ingredients
            )

        '''template = get_template('api/shoplist.html')
        html = template.render(output)
        pdf = pdfkit.from_string(html, False)

        filename = 'shopcart.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="' + filename + '"'
        )
        return response'''

        #pdfmetrics.registerfont(TTFont('droid-serif', 'fonts/LiberationSans-Regular.ttf'))
        '''buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(10, 700, output)
        p.showPage()
        p.save()
        buffer.seek(0)
        filename = 'shopcart.pdf'
        return FileResponse(buffer, as_attachment=True, filename=filename)'''

class IngredientsInRecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = IngredientInRecipeSerializer
