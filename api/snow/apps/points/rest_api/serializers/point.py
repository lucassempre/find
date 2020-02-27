from rest_framework import serializers
from django.contrib.auth.models import User
from snow.apps.points.models import Image, Category, Comment, Point
from django.utils.translation import gettext_lazy as _


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'file', 'comment', 'point',)
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'file',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'public', 'points',)
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'text', 'point', 'author',)
        
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'point', 'author',)

class MyPointSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    image         = ImageSerializer(required=False, many=True)
    author        = UserSerializer(required=False, read_only=True)
    class Meta:
        model  = Point
#        fields = ('pk', 'title', 'text', 'author', 'image', 'comment_count', 'long_position', 'lat_position')
        fields = "__all__"
    def get_comment_count(self, obj):
        return obj.comment.count()
    def get_author(self, obj):
        return obj.author.get()
      