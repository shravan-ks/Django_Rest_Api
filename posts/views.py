from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from posts.models import Post, Comment
from posts.serializers import PostSerializer, OwnerSerializer, CommentSerializer
from .permissions import IsOwnerPermission
User = get_user_model()


# CRUD Operations in API View Class Based
class PostView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Saved Form !"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        queryset = Post.objects.get(pk=pk)
        serializer = PostSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Saved Form !"}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        queryset = Post.objects.get(pk=pk)
        queryset.delete()
        return Response({"Message": "Deleted Form !"}, status=HTTP_204_NO_CONTENT)


# CRUD Operations in  Class Based Mixins
class PostMixinListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, pk, *args, **kwargs)


# Crud Operations Generic Class Based Views

# ListView
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)


# CreateView
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Permission Class
    permission_classes = (IsAuthenticated,)


# Detail View
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Delete View
class PostDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Update View
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Create custom Permissions
# Step: Create a permission.py
class PostDetailViewPermission(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # only allows to view if the data belongs to owner i.e owner = request.user
    permission_classes = (IsAuthenticated, IsOwnerPermission)


# Hyperlink Example
# Step Check out Serializers.py
class OwnerDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer


class CommentView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@csrf_exempt
# Csrf exempt means this function will not have csrf token for any forms
# ListView in Function method (def)
def post_list(request):
    if request.method == 'GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
# Csrf exempt means this function will not have csrf token for any forms
# DetailView in Function method (def)
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)


# Viewset And Routers
class Postviewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        AllowAny,
    )
