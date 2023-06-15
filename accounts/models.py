from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from PIL import Image as A_Image
from recipes.models import Ingredient, Recipe


class UserIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.nickname + self.ingredient.name


class User(AbstractUser):
    email = models.EmailField("이메일", blank=False)
    nickname = models.CharField("닉네임", max_length=8, blank=False, null=True)
    followers = models.ManyToManyField(
        "self", related_name="followings", symmetrical=False
    )
    def image_path(instance, filename):
        return f'accounts/profile/{instance.pk}/{filename}'
    profile_image = models.ImageField(upload_to=image_path, null=True, blank=True)
    fridge = models.ManyToManyField(
        Ingredient, through="UserIngredient", related_name="fridge_users", blank=True
    )
    birthdate = models.DateField("생년월일", null=True, blank=True)
    viewed_recipes = models.ManyToManyField(
        Recipe, related_name="viewed_users", blank=True
    )


    def process_image(profile_image):
        img = A_Image.open(profile_image)
        
        # 회전 메타데이터를 확인하여 이미지 회전
        if hasattr(img, '_getexif') and img._getexif():
            exif = dict(img._getexif().items())
            orientation = exif.get(0x0112)
            
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
        
        # 이미지 처리 및 저장
        img.thumbnail((800, 800))  # 이미지 크기 조정 등 필요한 처리
        img.save(profile_image.path)