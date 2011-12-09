from hashlib import md5
import json
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_unicode
from routeshout import *


# Best tutorial on decorators: http://stackoverflow.com/questions/739654/understanding-python-decorators
from routeshout.routeshout import StopTime

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
#        eugene_station_stop = 1310

        walnut = Stop(1651, self.LTD, name="walnut", api=self.api)
        eugene = Stop(1310, self.LTD, name="eugene", api=self.api)
#        walnut = self.get_stop_fake()

        result = {
            'walnut': walnut.times,
            'eugene': eugene.times,
        }
        return result

    @cacheable()
    def get_stop_times(self, id):
        stop = Stop(id, self.LTD, self.api)
        return Stop.times

    def get_stop_fake(self):
        json_data = """
        {"status":"ok","meta":{"timezone":"America/Los_Angeles"},"response":[{"type":"scheduled","route_short_name":"EmX","route_long_name":"EmX","arrival_time":"10:23 PM","departure_time":"10:23 PM","trip_id":"476847"},{"type":"scheduled","route_short_name":"EmX","route_long_name":"EmX","arrival_time":"10:40 PM","departure_time":"10:40 PM","trip_id":"478061"}]}
        """
        data = json.loads(json_data)
        times = data['response']
        l = []
        for t in times:
            l.append(StopTime(dict=t))

        stop = Stop(123, 'LTD')
        stop._times = l
        return stop

