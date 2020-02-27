from django.core.management.base import BaseCommand, CommandError
from snow.apps.points.models import Point
from snow.apps.points.utils.redis import * 
from django.conf import settings

GeoDb = SnowGeoRedis(settings.REDIS_HOST)
class Command(BaseCommand):
    help = 'Get points and set on redis'
    def handle(self, **options):
        [ GeoDb.set_point(point.long_position, point.lat_position, point.pk) for point in Point.objects.all() ]
