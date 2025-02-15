from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для управления постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            self.permission_denied(self.request,
                                   message="Изменение чужого поста запрещено.",
                                   code=403)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            self.permission_denied(self.request,
                                   message="Удаление чужого поста запрещено.",
                                   code=403)
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями."""
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            self.permission_denied(self.request,
                                   message="Изменение чужого "
                                           "комментария запрещено.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            self.permission_denied(self.request,
                                   message="Удаление чужого "
                                           "комментария запрещено.")
        instance.delete()


class CustomAuthToken(ObtainAuthToken):
    """Предоставляет токен пользователю."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
