from request_filters.utils import * 

def exempt_IPCheckMiddleware(func):
    """ view decorator, the sole purpose to is 'rename' the function to
    '_exempt_IPCheckMiddleware'.
    So we can identify functions those name is '_exempt_IPCheckMiddleware', to skip this view function from IPCheckMiddleware"""

    def _exempt_IPCheckMiddleware(*args, **kwargs):
        return func(*args, **kwargs)

    # copiedFunc = func
    # copiedFunc.__name__ = '_exempt_IPCheckMiddleware'
    return _exempt_IPCheckMiddleware


def prevent_anonymous_ip(func, block_vpn=setting("BLOCK_VPN", True), block_proxy=setting("BLOCK_PROXY", True), block_tor=setting("BLOCK_TOR", True), block_relay=setting("BLOCK_RELAY", True)):
    def innerFunction(*args, **kwargs):
        request = args[0]
        client_ip, is_routable = get_client_ip(request)
        userIp = getUserIpInfo(client_ip)
        if isAnonymousIP(userIp, block_vpn, block_proxy, block_tor, block_relay):
            if setting('IP_BLOCK_VIEW') is None:
                return HttpResponse("<h1>We can't allow your request, because you are using VPN or Proxy or Tor or Relay.</h1>", status=418)
            else:
                view = import_string(setting('IP_BLOCK_VIEW'))
                return view(request)
        else:
            return func(*args, **kwargs)
    return innerFunction