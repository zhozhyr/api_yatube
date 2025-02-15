from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list',
                                 'post': 'create'}),
         name='comment-list'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve',
                                 'put': 'update',
                                 'patch': 'partial_update',
                                 'delete': 'destroy'}),
         name='comment-detail'),
    path('v1/api-token-auth/',
         CustomAuthToken.as_view(), name='api_token_auth'),
]
