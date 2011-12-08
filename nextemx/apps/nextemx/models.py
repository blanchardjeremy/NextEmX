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
            cache_key = f.__name__
            if args and kwargs:
                cache_key = cache_key+':'+md5(':'.join(force_unicode(v) for v in (list(args) + kwargs.items()))).hexdigest()

            chunk = cache.get(cache_key)
            if chunk is None:
                chunk = f(self, *args, **kwargs)
                cache.set(cache_key, chunk, timeout)

            return chunk

        return inner

    return wrap



class NextEmX(object):
    LTD = 'ltd'
    CACHE_TIMEOUT = 60
    api = RouteShoutAPI(settings.ROUTESHOUT_API_KEY)

    def __init__(self):
        pass

    def jeremy(self):
#        routes = self.api.routes_getList(self.LTD)
        emx_route = 4656
#        stops = self.api.stops_getList(self.LTD, emx_route)

        walnut_times = self.jeremy_walnut()
        eugene_station_times = self.jeremy_eugene()

        result = {
            'walnut': walnut_times,
            'eugene': eugene_station_times,
        }
        return result
    
    @cacheable()
    def jeremy_walnut(self):
        walnut_stop = 1651
        return self.api.stops_getTimes(self.LTD, walnut_stop)

    def jeremy_eugene(self):
        eugene_station_stop = 1310
        key = 'eugene'
        if cache.get(key):
            return cache.get(key)
        else:
            val = self.api.stops_getTimes(self.LTD, eugene_station_stop)
            cache.set(key, val, self.CACHE_TIMEOUT)
            return val
