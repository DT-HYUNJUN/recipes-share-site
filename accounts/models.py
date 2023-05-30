from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from recipes.models import Ingredient


class User(AbstractUser):
    email = models.EmailField('이메일', blank=False)
    nickname = models.CharField('닉네임', max_length=8, blank=False, null=True)
    followers = models.ManyToManyField('self', related_name='followings', symmetrical=False)
    profile_image = ProcessedImageField(upload_to='profile/', processors=[ResizeToFill(300, 300)], format='JPEG', options={'quality': 80}, null=True, blank=True)
    fridge = models.ManyToManyField(Ingredient, related_name='fridge_users', blank=True)