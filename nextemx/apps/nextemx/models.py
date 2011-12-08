from hashlib import md5
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_unicode
from routeshout import RouteShoutAPI


# Best tutorial on decorators: http://stackoverflow.com/questions/739654/understanding-python-decorators
def cacheable(timeout=None, key=None):
    timeout = timeout if timeout else settings.CACHES['default']['TIMEOUT']

    def wrap(f):

        def inner(self, *args, **kwargs):
            key_parts = [self.__class__.__name__, f.__name__]
            if args or kwargs:
                key_parts.append(md5(':'.join(force_unicode(v) for v in (list(args) + kwargs.items()))).hexdigest())

            cache_key = ':'.join(key_parts)

            chunk = cache.get(cache_key)
            if chunk is None:
                chunk = f(self, *args, **kwargs)
                cache.set(cache_key, chunk, timeout)

            return chunk

        return inner

    return wrap



class NextEmX(object):
    LTD = 'ltd'
    api = RouteShoutAPI(settings.ROUTESHOUT_API_KEY)

    def __init__(self):
        pass

    def jeremy(self):
#        routes = self.api.routes_getList(self.LTD)
#        emx_route = 4656
#        stops = self.api.stops_getList(self.LTD, emx_route)

        walnut_stop = 1651
        eugene_station_stop = 1310
        walnut_times = self.get_stop_times(walnut_stop)
        eugene_station_times = self.get_stop_times(eugene_station_stop)

        result = {
            'walnut': walnut_times,
            'eugene': eugene_station_times,
        }
        return result

    @cacheable()
    def get_stop_times(self, id):
        return self.api.stops_getTimes(self.LTD, id)