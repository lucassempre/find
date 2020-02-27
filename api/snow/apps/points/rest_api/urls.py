from django.urls import path
from django.conf.urls import include
from .views import point_views
from rest_framework.schemas import get_schema_view

#from rest_framework.authtoken.views import obtain_auth_token
schema_view = get_schema_view(title="SnowApi")

urlpatterns = [
    path('schema/', schema_view),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
#   path('auth/', obtain_auth_token, name='api_token_auth'), 
    path('me/point/', point_views.MyPointsList.as_view(), name='api-my-point-list'),
    path('me/comment/', point_views.CommentListCreateAPIView.as_view(), name='api-my-comment-list'),
    path('me/image/', point_views.ImageListCreateAPIView.as_view(), name='api-my-images-list'),
  
    path('category/', point_views.CategoryListCreateAPIView.as_view(), name='api-category-list'),
    path('category/<int:pk>/', point_views.CategoryDetailsAPIView.as_view(), name='api-category-details'),
  
    path('comment/<uuid:pk>/', point_views.CommentDetailsAPIView.as_view(), name='api-comment-details'),
    path('image/<uuid:pk>/', point_views.ImageDetailsAPIView.as_view(), name='api-images-details'),
  
    path('point/<str:latitude>/<str:longitude>/radius/<int:radius>/', point_views.PointListRange.as_view()),
    path('point/<str:latitude>/<str:longitude>/radius/<int:radius>/category/<int:category>/', point_views.PointListRangeByCategory.as_view()),
    path('point/<uuid:pk>/', point_views.PointDetailsAPIView.as_view(), name='api-point-details'),
#    path('/point/<uuid:pk>/comment/', point_views.PointDetailsAPIView.as_view(), name='api-my-point-details'),
#    path('/point/<uuid:pk>/comment/<uuid:pk>/', point_views.PointDetailsAPIView.as_view(), name='api-my-point-details'),
    

  

  
]