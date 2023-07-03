from django.shortcuts import render, redirect
from request_filters.utils import * 


class IPCheckMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        # This code is executed just before the view is called to process the requests
        return request     

    def process_response(self, request, response):
        # After the view has finished executing, this code is executed to process the response. 
        return response

    def __call__(self, request):

        # Code to be executed for each request before the view (and later middleware) are called.
        request =  self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        response =  self.process_response(request, response)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
        if view_func.__name__ != "_exempt_IPCheckMiddleware":
            client_ip, is_routable = get_client_ip(request)
            userIp = getUserIpInfo(client_ip)
            if isAnonymousIP(userIp):
                if setting('IP_BLOCK_VIEW') is None:
                    return HttpResponse("<h1>We can't allow your request, because you are using VPN or Proxy or Tor or Relay.</h1>", status=418)
                else:
                    view = import_string(setting('IP_BLOCK_VIEW'))
                    return view(request)

    def process_template_response(self, request, response):
        # After the view has finished executing, this code is executed if the response contains a render() method
        return response

    def process_exception(self, request, exception):
        # This code is executed if an exception is raised
        return exception