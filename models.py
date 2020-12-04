from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

ITEM_CHOICES = (
    ('Cardboard','Cardboard'),
    ('Fruit Waste', 'Fruit Waste'),
    ('Vegetable Waste','Vegetable Waste'),
    ('Leftovers','Leftovers'),
    ('Coffee Grounds','Coffee Grounds'),
    ('Yard Waste','Yard Waste'),
    ('Animal Waste','Animal Waste'),
    ('Egg Shells','Egg Shells'),
)

class Group(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Group must be greater than 1 character")]
    )

    def __str__(self):
        return self.name

class LogEntry(models.Model):
    nickname = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")]
    )
    item = models.CharField(max_length=16, choices=ITEM_CHOICES, default='Cardboard')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='logentrys_owned')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='logentry_comments')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_logentrys')

    def __str__(self):
        return self.item

class Fav(models.Model) :
    logentry = models.ForeignKey(LogEntry, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('logentry', 'owner')

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    logentry = models.ForeignKey(LogEntry, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'