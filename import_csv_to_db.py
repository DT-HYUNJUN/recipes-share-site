import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pjt.settings")
django.setup()

import csv
from recipes.models import *
from accounts.models import User

with open("recipe_data/recipes.csv", "r", encoding="utf-8") as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for index, row in enumerate(csv_data):
        print(index, row[0])
        recipe = Recipe()
        recipe.title = row[0]
        recipe.user = User.objects.get(pk="1")
        recipe.content = row[2]
        recipe.category = row[3]
        recipe.image = row[4]
        recipe.time = row[5]
        recipe.difficulty = row[6]
        recipe.save()

        equip = Equip()
        equip.recipe = recipe

        i = 7
        while 1:
            # print(row[i])
            # seq_recipe_ingredient = f'recipe_ingredient_{i}'
            seq_recipe_ingredient = RecipeIngredient()

            if row[i] == "끝":
                break
            # print(row[i])
            ingre, qtt = row[i].split(",")

            my_ingre = Ingredient.objects.get_or_create(name=ingre)

            seq_recipe_ingredient.recipe = recipe
            seq_recipe_ingredient.ingredient = my_ingre[0]
            seq_recipe_ingredient.quantity = qtt
            seq_recipe_ingredient.save()
            i += 1
        i += 1

        if "전자레인지" in row[i]:
            equip.microwave = True
            i += 1
        if "가스레인지" in row[i]:
            equip.stove = True
            i += 1
        if "오븐" in row[i] or "오븐기" in row[i]:
            equip.oven = True
            i += 1
        if "에어프라이기" in row[i]:
            equip.air_fryer = True
            i += 1

        equip.save()

        while 1:
            # seq_recipe_step = f'recipe_step_{i}'
            seq_recipe_step = RecipeStep()
            if row[i] == "끝":
                break
            seq_recipe_step.recipe = recipe
            seq_recipe_step.detail = row[i]
            i += 1
            seq_recipe_step.save()
