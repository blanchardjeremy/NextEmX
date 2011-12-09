import urllib
import urllib2
import json

class RouteShoutAPI(object):
    api_url = 'http://api.routeshout.com/v1/%s?%s'
    api_key = None
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def request(self, method, data=None):
        data = data or {}
        # Add in the API key to the existing data
        data['key'] = self.api_key
        query_str = urllib.urlencode(data)
        # Build the full request URL
        request_url = self.api_url % (method, query_str)

        try:
            response = self._make_request(request_url)
        except Exception as inst:
            raise  # Just re-raise it!

        return response
    

    def _make_request(self, request_url):
        """
        Does the magic of actually sending the request and parsing the response
        """
        # TODO: I'm sure all kinds of error checking needs to go here
        response_raw = urllib2.urlopen(request_url)
        response_str = response_raw.read()
        response = json.loads(response_str)

        return response

    def agencies_getList(self):
        method = 'rs.agencies.getList'
        result = self.request(method)
        return result['response']
    
    
    def routes_getList(self, agency):
        method = 'rs.routes.getList'
        data = {
            'agency': agency,
        }
        result = self.request(method, data)
        return result['response']
    
    
    def stops_getList(self, agency, route):
        method = 'rs.stops.getList'
        data = {
            'agency': agency,
            'route': route,
        }
        result = self.request(method, data)
        return result['response']
    
    
    def stops_getInfo(self, agency, stop):
        method = 'rs.stops.getInfo'
        data = {
            'agency': agency,
            'stop': stop,
        }
        result = self.request(method, data)
        return result['response']
    
    
    def stops_getTimes(self, agency, stop):
        method = 'rs.stops.getTimes'
        data = {
            'agency': agency,
            'stop': stop,
        }
        result = self.request(method, data)
        return result['response']
    


class Stop(object):

    _times = []

    def __init__(self, id, agency, name="", api=None):
        self.id = id
        self.agency = agency
        self.name = name

        self.api = api

    def __unicode__(self):
        return u"%s - %s" % (self.id, self.agency)

    def __str__(self):
        return self.__unicode__()

    @property
    def times(self):
        """
        Returns an array of StopTime objects loaded from a dictionary passed by RouteSout
        """

        # Local caching
        if not self._times:
            self._times = []
            stoptimes_data = self.api.stops_getTimes(self.agency, self.id)
            for s in stoptimes_data:
                new_stop_time = StopTime(dict=s, stop=self)
                self._times.append(new_stop_time)
        return self._times

    @property
    def next(self):
        # Assumes top of list is next stop
        next = self.times[0] if self.times[0] else None
        return next

class StopTime(object):

    def __init__(self, departure_time=None, arrival_time=None, trip_id=None, route_long_name=None, route_short_name=None, dict=None, stop=None):

        if dict:
            departure_time =  dict['departure_time']
            arrival_time = dict['arrival_time']
            trip_id = dict['trip_id']
            route_long_name = dict['route_long_name']
            route_short_name = dict['route_short_name']

        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.trip_id = trip_id
        self.route_long_name = route_long_name
        self.route_short_name = route_short_name
        self.stop = stop

    def __unicode__(self):
        return u"%s - %s" % (self.departure_time, self.route_long_name)

    def __str__(self):
        return self.__unicode__()
