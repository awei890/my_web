from django.forms import ModelForm
from django.shortcuts import render, redirect
from manage_func import models


# Create your views here.


class user_form(ModelForm):
    '''modelform插件，用于用户注册'''

    class Meta:
        # 表是Users
        model = models.Users
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "user_image":
                field.widget.attrs = {}
                continue
            field.widget.attrs = {"class": "form-control"}


# ——————————上面为modelForm插件——————————
def index(request):
    return render(request, "./index.html")


def login(request):
    '''
    req:
        ip/index/login
    res:
        get -> login.html

        post -> 重定向到  ip/index/login   如果成功  ->  设置cookie  request.session["info"] = {"username": username, "password": password}
                                          如果失败  ->  用户名匹配失败  {'username': False}
                                                   ->  密码匹配失败    {‘password’: False}
    '''
    if request.method == "GET":
        return render(request, './login.html')

    else:
        # 拿到登录的数据并进行校验
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 与数据库进行匹配
        user = models.Users.objects.filter(name=username).first()
        if not user:
            # 匹配失败
            return render(request, 'login.html', {'username_error': "未找到用用户名"})

        if password != user.password:
            # 密码匹配失败
            return render(request, 'login.html', {'password_error': "密码匹配失败"})

        # 都成功的话就设定一个cookie
        request.session["user_info"] = {"username": username, "password": password}
        # 重定向到index页面
        return redirect("/index")


def register(request):
    '''
    req:
        ip/index/register
    res:
        get -> register.html
        post -> 注册成功后重定向  ip/index/login
    '''
    if request.method == "GET":
        form = user_form()
        return render(request, './register.html', {"form": form})
    else:
        data = user_form(request.POST, request.FILES)
        if data.is_valid():
            # 如果正确则保存
            data.save()
            # 返回login页面
            return redirect("../login")

        return render(request, './register.html', {"form": data})


def clear(request):
    '''
    清除专用,用于清除session
    req:
        ip/index/clear
    '''
    request.session.clear()
    return redirect("/index/login")
