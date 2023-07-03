from django.conf import settings
import requests
import json
from django.http import HttpResponse
from ipware import get_client_ip
from django.utils.module_loading import import_string


def setting(name, default=None):
    """
    Helper function to get a Django setting by name. If setting doesn't exists
    it will return a default.

    :param name: Name of setting
    :type name: str
    :param default: Value if setting is not found
    :returns: Setting's value
    """
    return getattr(settings, name, default)


def getUserIpInfo(ip_address):
    url = f"https://vpnapi.io/api/{ip_address}?key={setting('VPNAPI_KEY')}"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    ipInfo = requests.request("GET", url, headers=headers)
    ipInfo = json.loads(ipInfo.text)
    return ipInfo

def isAnonymousIP(userIp, block_vpn=setting("BLOCK_VPN", True), block_proxy=setting("BLOCK_PROXY", True), block_tor=setting("BLOCK_TOR", True), block_relay=setting("BLOCK_RELAY", True)):
    security = userIp.get('security', {})
    block_user = False
    if block_vpn and security.get('vpn') == True:
        block_user = True
    if block_proxy and security.get('proxy') == True:
        block_user = True
    if block_tor and security.get('tor') == True:
        block_user = True
    if block_relay and security.get('relay') == True:
        block_user = True
    return block_user