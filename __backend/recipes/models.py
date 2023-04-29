from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from users.models import UserCustomized


class Ingredients(models.Model):
    CAN = 'банка'
    LOAF = 'батон'
    BOTTLE = 'бутылка'
    TWIG = 'веточка'
    GRAM = 'г'
    PALM = 'горсть'
    SEMENT = 'долька'
    STAR = 'звездочка'
    CLOVE = 'зубчик'
    DROP = 'капля'
    KILO = 'кг'
    PIECE = 'кусок'
    LITRE = 'л'
    LEAF = 'лист'
    ML = 'мл'
    BAG = 'пакет'
    SACHET = 'пакетик'
    PACK = 'пачка'
    PLAST = 'пласт'
    UP2U = 'по вкусу'
    BEAM = 'пучок'
    SPOON = 'ст. л.'
    GLASS = 'стакан'
    STEM = 'стебель'
    POD = 'стручок'
    CARCASS = 'тушка'
    PACKAGE = 'упаковка'
    TEA_SPOON = 'ч. л.'
    ITEM = 'шт.'
    PINCH = 'щепотка'

    UNIT_CHOICES = (
        (CAN, 'банка'),
        (LOAF, 'батон'),
        (BOTTLE, 'бутылка'),
        (TWIG, 'веточка'),
        (GRAM, 'г'),
        (PALM, 'горсть'),
        (SEMENT, 'долька'),
        (STAR, 'звездочка'),
        (CLOVE, 'зубчик'),
        (DROP, 'капля'),
        (KILO, 'кг'),
        (PIECE, 'кусок'),
        (LITRE, 'л'),
        (LEAF, 'лист'),
        (ML, 'мл'),
        (BAG, 'пакет'),
        (SACHET, 'пакетик'),
        (PACK, 'пачка'),
        (PLAST, 'пласт'),
        (UP2U, 'по вкусу'),
        (BEAM, 'пучок'),
        (SPOON, 'ст. л.'),
        (GLASS, 'стакан'),
        (STEM, 'стебель'),
        (POD, 'стручок'),
        (CARCASS, 'тушка'),
        (PACKAGE, 'упаковка'),
        (TEA_SPOON, 'ч. л.'),
        (ITEM, 'шт.'),
        (PINCH, 'щепотка'),
    )
    name = models.CharField(max_length=254)
    units = models.TextField(max_length=10, choices=UNIT_CHOICES)

    class Meta:
        ordering = ("name",)
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.TextField(max_length=254)
    description = models.CharField(max_length=500)
    cooktime = models.IntegerField(verbose_name='Cooking time',  validators=(
            MinValueValidator(1, message='Minimum time is 1 minute'),
        ))
    image = models.ImageField('Image', upload_to='recipes/', blank=True)
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='tag'
    )
    author = models.ForeignKey(
        UserCustomized,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Author of the recipe',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("id",),
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.description


class IngredientInRecipe(models.Model):
    quantity = models.IntegerField(verbose_name='Quantity', validators=(
            MinValueValidator(1, 'Add at least 1 ingredient'),
        ))
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)
        constraints = (
            models.UniqueConstraint(fields=("recipe", "ingredient"),
                                    name="unique_ingredient"),)
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return self.quantity


class Tag(models.Model):
    name = models.CharField(max_length=254, unique=True,)
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                "^#([a-fA-F0-9]{6})",
                message="Only HEX-codes accepted",
            )
        ],
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("id",)
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug


class Favourites(models.Model):
    '''Favourite recipes model'''
    user = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='fav_adder',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fav_recipe',
        verbose_name='Recipe'
    )

    class Meta:
        ordering = ("-id",)
        constraints = (models.UniqueConstraint(fields=("user", "recipe"),
                                               name="unique_user_recipe"),)
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return self.user


class ShopList(models.Model):
    user = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='shopper',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoplist_recipe',
        verbose_name='Recipe'
    )

    class Meta:
        ordering = ("-id",)
        constraints = (models.UniqueConstraint(fields=("user", "recipe"),
                                               name="unique_user_list"),)
        verbose_name = 'Список покупок',

    def __str__(self):
        return self.recipe
