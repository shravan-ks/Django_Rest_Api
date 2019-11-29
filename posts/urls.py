from rest_framework.routers import DefaultRouter
from django.urls import path, include
from posts.views import Postviewset


# viewsets and Routers
router = DefaultRouter()

router.register('posts',Postviewset)

post_detail = Postviewset.as_view(
    {
        'get': 'list',
        'post': 'create',
    }
)


urlpatterns = [
    # gets all actions like get delete and update and urls too example /viewset/posts/ and viewset/posts/2 for deatil view
    path('', include(router.urls)),

    # this has custom defined actions as mentioned above in post_detail only performs get and post method
    path('custom/' , post_detail,name='custom')
]