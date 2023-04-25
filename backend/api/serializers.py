from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.models import UserCustomized, Follow
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.db.models import F
from recipes.models import (
    Ingredients,
    IngredientInRecipe,
    Recipe,
    Tag,
    ShopList,
    Favourites
)
import base64


class GetIsSubscribedMixin:
    '''User follow Mixin'''
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class GetIngredientsMixin:
    '''Recipe's Mixin.'''

    def get_ingredients(self, obj):
        '''Ingredients retrievement for recipes'''
        return obj.ingredients.values(
            'id',
            'name',
            'units',
            quantity=F('ingredientinrecipe__quantity'),
        )


class Base64ImageField(serializers.ImageField):
    '''Pictures decoding'''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostUserSerializer(UserCreateSerializer):
    '''User creation and change'''
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = UserCustomized
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = UserCustomized.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class GetUserSerializer(serializers.ModelSerializer):
    '''User information retrievement'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserCustomized
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
    read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class TagsSerializer(serializers.ModelSerializer):
    '''Tags' objects serialization. Tags list'''

    class Meta:
        model = Tag
        fields = 'id', 'name', 'color', 'slug'


class IngredientsSerializer(serializers.ModelSerializer):
    '''Ingredients' objects serialization. Ingredients list'''

    class Meta:
        model = Ingredients
        fields = 'id', 'name', 'units'


class GetRecipeSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    '''Recipes' objects serialization. Recipes list'''

    tags = TagsSerializer(many=True)
    author = GetUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'cooktime', 'image', 'ingredients',
            'tags', 'author', 'is_favorited', 'is_in_shopping_cart'
        )


class CreateUpdateRecipeSerializer(GetIngredientsMixin,
                                   serializers.ModelSerializer):
    '''Recipes' objects serialization. Recipes list'''
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'cooktime',
            'image', 'ingredients', 'tags', 'author'
        )
        read_only_fields = ('author',)

    def validate(self, data):
        '''Ingredients' validation for recipe.'''
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Add at least 1 ingredint.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, id=item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ingredient must be unique.'
                )
            if int(item['quantity']) < 1:
                raise serializers.ValidationError('Minimum quantity is 1 unit')
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_cooking_time(self, time):
        '''Cooking time validation.'''
        if int(time) < 1:
            raise serializers.ValidationError('Minimum time is 1 minute')
        return time

    def ingreds_and_tags_add(self, instance, **validate_data):
        '''Ingredient tags adding.'''
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=instance,
                    ingredient_id=ingredient['id'],
                    quantity=ingredient['quantity'],
                )
                for ingredient in ingredients
            ]
        )
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        return self.ingreds_and_tags_add(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = self.ingreds_and_tags_add(
            instance, ingredients=ingredients, tags=tags
        )
        return super().update(instance, validated_data)


class AddRecipeSerializer(serializers.ModelSerializer):
    '''Recipes objects serialization, add to favs&shopcart'''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooktime', 'image')
        read_only_fields = ('id', 'name', 'cooktime', 'image')


class FollowSerializer(GetIsSubscribedMixin, serializers.ModelSerializer):
    '''Follow objects serialization'''

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        '''Get author's recipes.'''
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if limit:
            queryset = queryset[: int(limit)]
        return AddRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()


class CheckFollowSerializer(serializers.ModelSerializer):
    '''Validation of the following process.'''

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, obj):
        '''Following process validation.'''
        user = obj['user']
        author = obj['author']
        subscribed = user.follower.filter(author=author).exists()

        if self.context['request'].method == 'POST':
            if user == author:
                raise serializers.ValidationError(
                    'Self following is not allowed'
                )
            if subscribed:
                raise serializers.ValidationError(
                    'You have alredy unfollowed this author'
                )
        if self.context['request'].method == 'DELETE':
            if user == author:
                raise serializers.ValidationError(
                    'You can\'t unfollow yourself'
                )
            if not subscribed:
                raise serializers.ValidationError(
                    {'errors': 'You have already unfollowed this author'}
                )
        return obj


class CheckFavouriteSerializer(serializers.ModelSerializer):
    '''Serialization of favourites and check addind to favourites.'''

    user = serializers.PrimaryKeyRelatedField(
        queryset=UserCustomized.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Favourites
        fields = ('user', 'recipe')

    def validate(self, obj):
        '''Add to favourites validation.'''
        user = self.context['request'].user
        recipe = obj['recipe']
        favorite = user.fav_adder.filter(recipe=recipe).exists()

        if self.context['request'].method == 'POST' and favorite:
            raise serializers.ValidationError(
                'This recipe is already in favourites.'
            )
        if self.context['request'].method == 'DELETE' and not favorite:
            raise serializers.ValidationError(
                'No such a recipe in your favourites.'
            )
        return obj


class CheckShopCartSerializer(serializers.ModelSerializer):
    '''Shoplist objects serialization'''

    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserCustomized.objects.all()
    )

    class Meta:
        model = ShopList
        fields = ('user', 'recipe')

    def validate(self, obj):
        '''Adding a recipe into shopcart validation'''
        user = self.context['request'].user
        recipe = obj['recipe']
        shop_list = user.shopper.filter(recipe=recipe).exists()

        if self.context['request'].method == 'POST' and shop_list:
            raise serializers.ValidationError(
                'Recipe in shoplist alredy.'
            )
        if self.context['request'].method == 'DELETE' and not shop_list:
            raise serializers.ValidationError('Recipe not in shoplist.')
        return obj
