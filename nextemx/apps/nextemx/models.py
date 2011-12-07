from django.db import models
from django.conf import settings
from routeshout import RouteShoutAPI

# Create your models here.

class NextEmX(object):
    LTD = 'ltd'
    api = RouteShoutAPI(settings.ROUTESHOUT_API_KEY)

    def __init__(self):
        pass

    def jeremy(self):
#        routes = self.api.routes_getList(self.LTD)
        emx_route = 4656
#        stops = self.api.stops_getList(self.LTD, emx_route)
        walnut_stop = 1651
        eugene_station_stop = 1310

        walnut_times = self.api.stops_getTimes(self.LTD, walnut_stop)
        eugene_station_times = self.api.stops_getTimes(self.LTD, eugene_station_stop)

        result = {
            'walnut': walnut_times,
            'eugene':eugene_station_times,
        }
        return result
