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


class Recipe(models.Model):
    name = models.TextField(max_length=254)
    description = models.CharField(max_length=500)
    cooktime = models.IntegerField(verbose_name='Cooking time',  validators=(
            MinValueValidator(1),
        ))
    image = models.ImageField('Image', upload_to='recipes/', blank=True)
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        # through_fields=('recipe', 'ingredient'),
        verbose_name='ingredient'
    )
    tags = models.ManyToManyField(
        'Tag',
        # related_name='recipes',
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

    # pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ("id",)


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
