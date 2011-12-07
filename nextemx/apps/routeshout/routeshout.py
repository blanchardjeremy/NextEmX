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
    
