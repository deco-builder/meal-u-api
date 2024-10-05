from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..services.like_and_comment import RecipeLikeAndCommentService, MealKitLikeAndCommentService
from ..models import Recipe, MealKit
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsClientUser
from ..serializers.like_and_comment import RecipeCommentSerializer, MealKitCommentSerializer

class RecipeLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            like = RecipeLikeAndCommentService.like_recipe(request.user, recipe)
            return Response(prepare_success_response({"message": "Recipe liked successfully."}), status=status.HTTP_201_CREATED)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class RecipeCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request, recipe_id):
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({"error": "Comment is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            comment = RecipeLikeAndCommentService.comment_on_recipe(request.user, recipe, comment_text)
            return Response(prepare_success_response({"message": "Comment added successfully.", "data": comment_text}), status=status.HTTP_201_CREATED)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class RecipeStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]
    
    def get(self, request, recipe_id):
        try:
            likes_count = RecipeLikeAndCommentService.get_recipe_likes_count(recipe_id)
            comments_count = RecipeLikeAndCommentService.get_recipe_comments_count(recipe_id)

            return Response(prepare_success_response({
                'likes_count': likes_count,
                'comments_count': comments_count
            }), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RecipeCommentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, recipe_id):
        try:
            comments = RecipeLikeAndCommentService.get_all_recipe_comments(recipe_id)
            serializer = RecipeCommentSerializer(comments, many=True)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MealKitLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request, mealkit_id):
        try:
            mealkit = MealKit.objects.get(id=mealkit_id)
            like = MealKitLikeAndCommentService.like_mealkit(request.user, mealkit)
            return Response(prepare_success_response({"message": "MealKit liked successfully."}), status=status.HTTP_201_CREATED)
        except MealKit.DoesNotExist:
            return Response({"error": "MealKit not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class MealKitCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request, mealkit_id):
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({"error": "Comment is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            mealkit = MealKit.objects.get(id=mealkit_id)
            
            comment = MealKitLikeAndCommentService.comment_on_mealkit(request.user, mealkit, comment_text)
            
            return Response(prepare_success_response(
                {"message": "Comment added successfully.", "data": comment_text}),
                status=status.HTTP_201_CREATED
            )
        except MealKit.DoesNotExist:
            return Response({"error": "MealKit not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class MealKitStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]
    
    def get(self, request, mealkit_id):
        try:
            likes_count = MealKitLikeAndCommentService.get_mealkit_likes_count(mealkit_id)
            comments_count = MealKitLikeAndCommentService.get_mealkit_comments_count(mealkit_id)

            return Response(prepare_success_response({
                'likes_count': likes_count,
                'comments_count': comments_count
            }), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class MealKitCommentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, mealkit_id):
        try:
            comments = MealKitLikeAndCommentService.get_all_mealkit_comments(mealkit_id)
            serializer = MealKitCommentSerializer(comments, many=True)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)    