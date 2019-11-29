from django.contrib import admin
from django.urls import path, include
from posts.views import PostView, post_list, post_detail, PostMixinListView, PostListView, PostDetailView, \
    PostDestroyView, PostUpdateView, PostCreateView, PostDetailViewPermission, OwnerDetailView, CommentView

urlpatterns = [
    path('admin/', admin.site.urls),
    #   Rest API Urls
    path('api-auth/', include('rest_framework.urls')),

    #   Function Based view
    path('api/post_list', post_list, name='post-list'),
    path('api/post_detail/<int:pk>', post_detail, name='post-detail'),

    #   Class Based API VIEW
    path('api/posts', PostView.as_view(), name='post-view'),
    path('api/posts/<int:pk>', PostView.as_view(), name='post-view'),

    #   Class Based Mixins Views
    path('api/posts/mixin', PostMixinListView.as_view(), name='post-view-mixin'),
    path('api/posts/mixin/<int:pk>', PostMixinListView.as_view(), name='post-view-mixin'),

    #   Generic Class Based View
    path('api/posts/generic', PostListView.as_view(), name='post-list-view'),
    path('api/posts/generic/create', PostCreateView.as_view(), name='post-list-view'),
    path('api/posts/generic/<int:pk>', PostDetailView.as_view(), name='post-detail-view'),
    path('api/posts/generic/delete/<int:pk>', PostDestroyView.as_view(), name='post-delete-view'),
    path('api/posts/generic/update/<int:pk>', PostUpdateView.as_view(), name='post-update-view'),

    #   Custom Permission Detail View
    path('api/posts/permission/<int:pk>', PostDetailViewPermission.as_view(), name='post-detail-permission'),

    #   Hyperlinks
    path('api/owner/<pk>', OwnerDetailView.as_view(), name='owner-view'),
    path('api/comment/<pk>', CommentView.as_view(), name='comment-view'),

#     Viewset and Routert
    path('viewset/', include('posts.urls'))
]
