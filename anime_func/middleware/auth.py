from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————


class Manage_login(MiddlewareMixin):
    '''管理用户登录中间件'''

    def process_request(self, request):
        return

    def process_response(self, request, response):
        return response

# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
