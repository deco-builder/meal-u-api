import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, Recipe, MealKit
from django.contrib.auth import get_user_model
from django.db.models import Count
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsClientUser
from rest_framework.permissions import IsAuthenticated

User = get_user_model()
# Recipe Like Consumer
class LikeRecipeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.recipe_id = self.scope['url_route']['kwargs']['recipe_id']
        await self.channel_layer.group_add(
            f"recipe_{self.recipe_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"recipe_{self.recipe_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        recipe = await self.get_recipe(self.recipe_id)
        user = self.scope["user"]
        liked = await self.toggle_like(recipe, user)

        likes_count = await self.get_likes_count(recipe)
        comments_count = await self.get_comments_count(recipe)

        await self.channel_layer.group_send(
            f"recipe_{self.recipe_id}",
            {
                'type': 'recipe_stats_updated',
                'user_id': user.id,
                'recipe_id': self.recipe_id,
                'likes_count': likes_count,
                'comments_count': comments_count
            }
        )

    async def recipe_stats_updated(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'recipe_id': event['recipe_id'],
            'likes_count': event['likes_count'],
            'comments_count': event['comments_count'],
        }))

    @database_sync_to_async
    def get_recipe(self, recipe_id):
        return Recipe.objects.get(id=recipe_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def toggle_like(self, recipe, user):
        liked, created = RecipeLike.objects.get_or_create(recipe=recipe, user=user)
        if not created:
            liked.delete()
            return False
        return True

    @database_sync_to_async
    def get_likes_count(self, recipe):
        return RecipeLike.objects.filter(recipe=recipe).count()

    @database_sync_to_async
    def get_comments_count(self, recipe):
        return RecipeComment.objects.filter(recipe=recipe).count()


# Recipe Comment Consumer
class CommentRecipeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.recipe_id = self.scope['url_route']['kwargs']['recipe_id']
        await self.channel_layer.group_add(
            f"recipe_{self.recipe_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"recipe_{self.recipe_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = data['comment']

        recipe = await self.get_recipe(self.recipe_id)
        user = self.scope["user"]
        await self.add_comment(recipe, user, comment)

        likes_count = await self.get_likes_count(recipe)
        comments_count = await self.get_comments_count(recipe)

        await self.channel_layer.group_send(
            f"recipe_{self.recipe_id}",
            {
                'type': 'recipe_stats_updated',
                'user_id': user.id,
                'recipe_id': self.recipe_id,
                'likes_count': likes_count,
                'comments_count': comments_count
            }
        )

    async def recipe_stats_updated(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'recipe_id': event['recipe_id'],
            'likes_count': event['likes_count'],
            'comments_count': event['comments_count'],
        }))

    @database_sync_to_async
    def get_recipe(self, recipe_id):
        return Recipe.objects.get(id=recipe_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def add_comment(self, recipe, user, comment):
        return RecipeComment.objects.create(recipe=recipe, user=user, comment=comment)

    @database_sync_to_async
    def get_likes_count(self, recipe):
        return RecipeLike.objects.filter(recipe=recipe).count()

    @database_sync_to_async
    def get_comments_count(self, recipe):
        return RecipeComment.objects.filter(recipe=recipe).count()


# MealKit Like Consumer
class LikeMealKitConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mealkit_id = self.scope['url_route']['kwargs']['mealkit_id']
        await self.channel_layer.group_add(
            f"mealkit_{self.mealkit_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"mealkit_{self.mealkit_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        mealkit = await self.get_mealkit(self.mealkit_id)
        user = self.scope["user"]
        liked = await self.toggle_like(mealkit, user)

        likes_count = await self.get_likes_count(mealkit)
        comments_count = await self.get_comments_count(mealkit)

        await self.channel_layer.group_send(
            f"mealkit_{self.mealkit_id}",
            {
                'type': 'mealkit_stats_updated',
                'user_id': user.id,
                'mealkit_id': self.mealkit_id,
                'likes_count': likes_count,
                'comments_count': comments_count
            }
        )

    async def mealkit_stats_updated(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'mealkit_id': event['mealkit_id'],
            'likes_count': event['likes_count'],
            'comments_count': event['comments_count'],
        }))

    @database_sync_to_async
    def get_mealkit(self, mealkit_id):
        return MealKit.objects.get(id=mealkit_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def toggle_like(self, mealkit, user):
        liked, created = MealKitLike.objects.get_or_create(mealkit=mealkit, user=user)
        if not created:
            liked.delete()
            return False
        return True

    @database_sync_to_async
    def get_likes_count(self, mealkit):
        return MealKitLike.objects.filter(mealkit=mealkit).count()

    @database_sync_to_async
    def get_comments_count(self, mealkit):
        return MealKitComment.objects.filter(mealkit=mealkit).count()


# MealKit Comment Consumer
class CommentMealKitConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mealkit_id = self.scope['url_route']['kwargs']['mealkit_id']
        await self.channel_layer.group_add(
            f"mealkit_{self.mealkit_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"mealkit_{self.mealkit_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = data['comment']

        mealkit = await self.get_mealkit(self.mealkit_id)
        user = self.scope["user"]
        await self.add_comment(mealkit, user, comment)

        likes_count = await self.get_likes_count(mealkit)
        comments_count = await self.get_comments_count(mealkit)

        await self.channel_layer.group_send(
            f"mealkit_{self.mealkit_id}",
            {
                'type': 'mealkit_stats_updated',
                'user_id': user.id,
                'mealkit_id': self.mealkit_id,
                'likes_count': likes_count,
                'comments_count': comments_count
            }
        )

    async def mealkit_stats_updated(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'mealkit_id': event['mealkit_id'],
            'likes_count': event['likes_count'],
            'comments_count': event['comments_count'],
        }))

    @database_sync_to_async
    def get_mealkit(self, mealkit_id):
        return MealKit.objects.get(id=mealkit_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def add_comment(self, mealkit, user, comment):
        return MealKitComment.objects.create(mealkit=mealkit, user=user, comment=comment)

    @database_sync_to_async
    def get_likes_count(self, mealkit):
        return MealKitLike.objects.filter(mealkit=mealkit).count()

    @database_sync_to_async
    def get_comments_count(self, mealkit):
        return MealKitComment.objects.filter(mealkit=mealkit).count()