from django.db import models
from django.core.validators import MinValueValidator
from users.models import UserCustomized


class Ingredients(models.Model):
    GRAMM = 'грамм'
    SPOON = 'ст. л.'
    MLL = 'мл.'
    PIECES = 'шт.'
    UP2U = 'по вкусу'
    A_BIT = 'щепотка'
    UNIT_CHOICES = (
        (GRAMM, 'грамм'),
        (SPOON, 'ст. л.'),
        (MLL, 'мл.'),
        (PIECES, 'шт.'),
        (UP2U, 'по вкусу'),
        (A_BIT, 'щепотка')
    )
    name = models.CharField(max_length=254)
    units = models.TextField(max_length=10, choices=UNIT_CHOICES)


class Recipe(models.Model):
    name = models.TextField(max_length=254)
    description = models.CharField(max_length=500)
    cooktime = models.IntegerField(verbose_name='Cooking time',  validators=(
            MinValueValidator(1),
        ))
    image = models.ImageField('Image', upload_to='recipes/', blank=True)
    ingredient = models.ManyToManyField(
        Ingredients,
        related_name='ingredient',
        verbose_name='ingredient'
    )
    tag = models.ManyToManyField('Tag', related_name='tag', verbose_name='tag')
    author = models.ForeignKey(
        UserCustomized,
        on_delete=models.SET_NULL,
        related_name='author',
        verbose_name='Author of the recipe',
        blank=True,
        null=True
    )
    quantity = models.IntegerField(verbose_name='Quantity', validators=(
            MinValueValidator(1),
        ))
    # pub_date = models.DateTimeField('Дата создания', auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=254)
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)


class Favourites(models.Model):
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


class Follow(models.Model):
    user = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='User'
    )
    author = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Post author'
    )

    class Meta:
        constraints = (models.UniqueConstraint(fields=('user_id',
                                                       'author_id'),
                                               name='unique_following'),)

    def __str__(self):
        return self.user
