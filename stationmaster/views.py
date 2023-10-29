from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from stationmaster import models
from utils import Pagination
import markdown


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


def my_blogs(request):
    '''
    req:
        ip/index/my_blogs       如果无参数，返回博客索引页
                                如果有参数 {“name”:"博客的名字"}
                                        {“page”:"1"}                            ->  返回所有blog中的10个blog
                                        {"classification": "分类", “page”:"1"}   ->  返回特定分类的10个blog
    res:
        返回blogposts的html文件
    '''


    if request.GET.get("name"):
        name = request.GET.get("name")
        blog = models.my_bolgs.objects.filter(name=name)[0]
        data = markdown.markdown(blog.content, extensions=[
            'markdown.extensions.extra',  # 用于标题、表格、引用这些基本转换
            'markdown.extensions.codehilite',  # 用于语法高亮
            'markdown.extensions.toc',  # 用于生成目录
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
            'markdown.extensions.tables',
            'markdown.extensions.admonition',
            'markdown.extensions.legacy_attrs',
            'markdown.extensions.legacy_em',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.smarty',
            'markdown.extensions.wikilinks'
        ])
        return render(request, "blogs/blog.html", {"data": data})

    if request.GET.get("classification") and request.GET.get("page"):
        '''从分类的blogs选10个'''
        classify = request.GET.get("classification")
        page = int(request.GET.get("page"))
        # 拿到所有blog对象
        blogs = models.my_bolgs.objects.filter(classification=classify)

        if page > blogs.count() // 10 + 1:
            # 如果前往的页面比页面总数还大，则返回错误信息
            return redirect(to="/index/errors")

        blogs_list = blogs[page - 1: page * 10 - 1]
        data, cursor = Pagination.page_navigation(page, blogs.count() // 10 + 1, 5)

        return render(request, "blogs/my_blogs.html", {"blogs": blogs_list, "pages": data})

    if request.GET.get("page"):
        '''从全部blogs中选10个'''
        page = int(request.GET.get("page"))
        # 拿到所有blog对象
        blogs = models.my_bolgs.objects.all()

        if page > blogs.count() // 10 + 1:
            # 如果前往的页面比页面总数还大，则返回错误信息
            return redirect("/index/errors")

        blogs_list = blogs[page - 1: page * 10 - 1]
        data, cursor = Pagination.page_navigation(page, blogs.count() // 10 + 1, 5)

        return render(request, "blogs/my_blogs.html", {"blogs": blogs_list, "pages": data})


def clear(request):
    '''
    清除专用,用于清除session
    req:
        ip/index/clear
    '''
    request.session.clear()
    return redirect("/index/login")


def errors(request):
    """
    req:
        ip/index/errors     传递参数：{type:1, content=错误内容}
                            如果没有参数，则返回自己的404页面
    res:
        无
    """
    if request.GET.get("type") and request.GET.get("content"):
        type_error = request.GET.get("type")
        content = request.GET.get("content")
        models.Error_log.objects.create(
            error_type=type_error,
            error_content=content
        )
        return JsonResponse({})

    return render(request, "errors.html")


def test(req):
    return render(req, "new.html")
