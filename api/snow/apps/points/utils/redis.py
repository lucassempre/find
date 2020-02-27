import logging
import redis

log = logging.getLogger('SnowGeoRedis')

class SnowGeoRedis(object):
    __conn = None
    """
    Init the class objects
    """
    def __init__(self, host='localhost', port=6379, lists='points', socket_connect_timeout=1):
        self.host    = host
        self.port    = port
        self.lists   = lists
        self.timeout = socket_connect_timeout
        self.check_connection()
    """
    This a function make a connection of redis
    """
    def __new_connection(self):
        self.__conn = redis.Redis(host = self.host, port = self.port, socket_connect_timeout = self.timeout)
    """
    This a function check redis connect by ping
    :return: Function redis 
    """    
    def new_ping(self):
        return self.__conn.ping()
    """
    This a function check connection on redis and connect
    :return: False or True
    """             
    def check_connection(self):
        if not self.__conn:
            self.__new_connection()
        try:
            self.__conn.ping()
            return True
        except redis.exceptions.ConnectionError as r_con_error:
            log.error("Redis connection error:" + r_con_error)
            return False
    """
    This a function return list of points
    :params latitude: this a referencial position 
    :params longitude: this a referencial position
    :params radius: this is a perimeter of search by km
    :return: List 
    """
    def get_points(self, latitude=0, longitude=0, radius=0):
        try:
            return [point.decode('UTF8') for point in self.__conn.georadius(self.lists, str(latitude), str(longitude), str(radius), 'km')]
        except:
            log.error("Get redis points error: lat{} long{} radius{}".format(latitude, longitude, radius))
            return False
    """
    This a function save a points on redis
    :params latitude: this a referencial position 
    :params longitude: this a referencial position
    :params pk: Point id on other db
    :return: False or True
    """
    def set_point(self, latitude, longitude, pk):
        try:
            return self.__conn.geoadd(self.lists, str(latitude), str(longitude), str(pk))
        except:
            log.error("Add point on redis error: " + str(pk) )
            return False
    """
    This a function reomve points on redis
    :params pk: Point id on other db
    :return: False or True
    """    
    def remove_point(self, pk):
        try:
            return self.__conn.zrem(self.lists, str(pk))
        except:
            log.error("Remove redis point error: " + str(pk))
            return False
    """
    This a function remove and save a point on redis
    :params latitude: this a new referencial position 
    :params longitude: this a new referencial position
    :params pk: Point id on other db is fixed
    :return: False or True
    """
    def update_point(self, latitude, longitude, pk):
        if (self.remove_point(pk)) and (self.set_point(latitude, longitude, pk)):
            return True
        else:
            return False