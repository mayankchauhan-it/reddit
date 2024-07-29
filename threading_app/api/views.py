from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from post.models import Post, UserInterest, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = ""
        try:
            user_interests = UserInterest.objects.get(user=request.user)
            categories = user_interests.categories.all()
            print(len(categories))
            if len(categories) > 0:
                posts = Post.objects.filter(category__in=categories).order_by("-id")
                print("User interests found, filtering posts by categories")
            else:
                posts = Post.objects.all().order_by("-id")
                print("No user interests found, showing all posts")
        except UserInterest.DoesNotExist:
            posts = Post.objects.all().order_by("-id")
            print("No user interests found, showing all posts")

        paginator = PostPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'GET':
        parent_id = request.query_params.get('parent')
        if parent_id:
            try:
                parent_comment = Comment.objects.get(pk=parent_id, post=post)
                comments = parent_comment.replies.all()
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)
            except Comment.DoesNotExist:
                return Response({"detail": "Parent comment not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            comments = post.comments.filter(parent=None)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['post'] = post_id
        data['author'] = request.user.id  

        if 'parent' in data and data['parent']:
            try:
                parent_comment = Comment.objects.get(pk=data['parent'])
                if parent_comment.post != post:
                    return Response({"detail": "Parent comment does not belong to this post."}, status=status.HTTP_400_BAD_REQUEST)
            except Comment.DoesNotExist:
                return Response({"detail": "Parent comment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if comment.author != request.user:
        return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)