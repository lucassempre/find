from django.db import models
from django.contrib.auth.models import User
from snow.apps.common.models import CoreModel
#from django.utils.translation import gettext_lazy as _

"""
Model of category
One category have a many Points.
"""
class Category(models.Model):
    name   = models.CharField(max_length=100, unique=True)
    public = models.BooleanField(default=False)
    def __str__(self):
        return self.name
"""
Model of Points
One point have a one category, author. 
One point have a many comments, images.
"""    
class Point(CoreModel):
    title         = models.CharField(max_length=100)
    text          = models.TextField()
    long_position = models.DecimalField (max_digits=10, decimal_places=7)
    lat_position  = models.DecimalField (max_digits=10, decimal_places=7)
    author        = models.ForeignKey(User, related_name='points', on_delete=models.CASCADE, blank=True, null=True)
    category      = models.ForeignKey(Category, related_name='points', on_delete=models.CASCADE, blank=True, null=True)
"""
Model of Bookmarks
One bookmark have a many Points.
One bookmark have a one author.
"""
class Bookmark(CoreModel):
    point  = models.ForeignKey(Point, related_name='bookmark', related_query_name="bookmarks", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='bookmark', related_query_name="bookmarks", on_delete=models.CASCADE, blank=True, null=False)
"""
Model of Comments
One comment have a one author, point
"""
class Comment(CoreModel):
    text   = models.TextField()
    point  = models.ForeignKey(Point, related_name='comment', related_query_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comment', related_query_name="comments", on_delete=models.CASCADE, blank=True, null=True)
"""
Model of Images
One image have a one file, and one point or comment.
"""
class Image(CoreModel):
    file    = models.ImageField(upload_to='images/')
    comment = models.ForeignKey(Comment, related_name='image', related_query_name="images", on_delete=models.CASCADE, blank=True, null=True)
    point   = models.ForeignKey(Point, related_name='image', related_query_name="images", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.file.name
