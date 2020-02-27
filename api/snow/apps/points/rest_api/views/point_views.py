from rest_framework import permissions, exceptions
from rest_framework import filters
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from snow.apps.points.models import Point
from snow.apps.points.rest_api.serializers.point import *
from snow.apps.points.utils.redis import * 
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

GeoDb = SnowGeoRedis(settings.REDIS_HOST)

class PointListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of points or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyPointSerializer
    queryset = Point.objects.active()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
#        r.zrem('points', str(instance.pk))
#        r.geoadd('points', str(instance.long_position), str(instance.lat_position), str(instance.pk))
        GeoDb.set_point(instance.long_position, instance.lat_position, instance.pk)
        
class PointListRange(ListAPIView):
    """
    API view to retrieve list of points over radius
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyPointSerializer
    def get_queryset(self):
        longitude = self.kwargs.get('longitude')
        latitude  = self.kwargs.get('latitude')
        radius    = self.kwargs.get('radius')
 #       points = [x.decode('UTF8') for x in r.georadius('points', str(latitude), str(longitude), str(radius), 'km')]
        points = GeoDb.get_points(latitude, longitude, radius)
        return Point.objects.filter(pk__in=points)

class PointListRangeByCategory(ListAPIView):
    """
    API view to retrieve list of points over radius
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyPointSerializer
    def get_queryset(self):
        longitude = self.kwargs.get('longitude')
        latitude  = self.kwargs.get('latitude')
        radius    = self.kwargs.get('radius')
        categoryt = self.kwargs.get('category')
#        points = [x.decode('UTF8') for x in r.georadius('points', str(latitude), str(longitude), str(radius), 'km')]
        points = GeoDb.get_points(latitude, longitude, radius)
        return Point.objects.filter(pk__in=points, category=categoryt)

class PointDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete point
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyPointSerializer
    queryset = Point.objects.active()
    def perform_update(self, serializer):
        original_object = self.get_object()
        if(original_object.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        serializer = serializer.save()
        GeoDb.update_point(serializer.lat_position, serializer.long_position, serializer.pk)
#        r.zrem('points', str(serializer.pk))
#        r.geoadd('points', str(serializer.long_position), str(serializer.lat_position), str(serializer.pk))
    def perform_destroy(self, instance):
        if(instance.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity')
        GeoDb.remove_point(instance.pk)
#        r.zrem('points', str(instance.pk))
        instance.delete()

class MyPointsList(ListCreateAPIView):
    """
    API view to retrieve list of my points
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyPointSerializer
    def get_queryset(self):
        return Point.objects.active().filter(author=self.request.user)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        GeoDb.set_point(instance.long_position, instance.lat_position, instance.pk)

class CommentListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of comments or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.active()
    
class CommentDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve list of comments or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.active()
    def perform_update(self, serializer):
        original_object = self.get_object()
        if(original_object.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        serializer = serializer.save()
    def perform_destroy(self, instance):
        if(instance.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        instance.delete()

class ImageListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of images or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    def get_queryset(self):
        return Comment.objects.active()
      
class ImageDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve list of images or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    def get_queryset(self):
        return Image.objects.active()
    def perform_update(self, serializer):
        original_object = self.get_object()
        if(original_object.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        serializer = serializer.save()
    def perform_destroy(self, instance):
        if(instance.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        instance.delete()

class CategoryListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of categories or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()
    
class CategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve list of categories or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()
    def perform_update(self, serializer):
        original_object = self.get_object()
        if(original_object.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        serializer = serializer.save()
    def perform_destroy(self, instance):
        if(instance.author != self.request.user):
           raise exceptions.PermissionDenied(detail='Not your entity') 
        instance.delete()
    
class BookmarkListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of categories or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer
    def get_queryset(self):
        return Bookmark.objects.all().filter(author=self.request.user)
    
class BookmarkDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve list of categories or create new
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer
    def get_queryset(self):
        return Bookmark.objects.all().filter(author=self.request.user)
    def perform_update(self, serializer):
        original_object = self.get_object()
        if(original_object.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
            serializer = serializer.save()
    def perform_destroy(self, instance):
        if(instance.author != self.request.user):
            raise exceptions.PermissionDenied(detail='Not your entity') 
        instance.delete()
