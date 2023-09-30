from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


"""
class User_login(MiddlewareMixin):
    '''用户登录中间件'''

    def process_request(self, request):
        if request.path_info.startswith("/index"):
            '''如果是/index开头，拦截'''

            if request.path_info == "/index/login" or request.path_info == "/index/login/":
                # 判定是否为登录界面，如果是，则通过
                return

            user_info = request.session.get("info")
            # 拿cookie的信息

            if not user_info:
                # 如果没有cookie（即信息为空），拦截跳转login
                return redirect("/index/login")
            # 否则正常通过
            return

        else:
            '''如果不是index开头，通过'''
            return

    def process_response(self, request, response):
        return response
"""

# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————


class Manage_login(MiddlewareMixin):
    '''管理用户登录中间件'''

    def process_request(self, request):
        if request.path_info.startswith("/manage"):
            '''如果是 /manage开头'''

            if request.path_info == "/manage/login" or request.path_info == "/manage/login/":
                # 如果去登录页面，通过
                return

            manager_info = request.session.get("manage_info")
            if not manager_info:
                # 如果无cookie
                return redirect("/manage/login")

            # 否则正常通过
            return

        else:
            '''不是manage开头'''
            return

    def process_response(self, request, response):
        return response

# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————

