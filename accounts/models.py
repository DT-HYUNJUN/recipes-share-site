from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from recipes.models import Ingredient


class UserIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.user.nickname + self.ingredient.name


class User(AbstractUser):
    email = models.EmailField('이메일', blank=False)
    nickname = models.CharField('닉네임', max_length=8, blank=False, null=True)
    followers = models.ManyToManyField('self', related_name='followings', symmetrical=False)
    profile_image = ProcessedImageField(upload_to='profile/', processors=[ResizeToFill(300, 300)], format='JPEG', options={'quality': 80}, null=True, blank=True)
    fridge = models.ManyToManyField(Ingredient, through='UserIngredient', related_name='fridge_users', blank=True)
    birthdate = models.DateField('생년월일', null=True, blank=True)