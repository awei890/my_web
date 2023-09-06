from basic_func import models as m1
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from manage_func import models as m2
from static.plugins.video_url import yinghua


class user_form(ModelForm):
    '''modelform插件，用于用户注册'''

    class Meta:
        # 表是Users
        model = m1.Users
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "user_image":
                field.widget.attrs = {}
                continue
            field.widget.attrs = {"class": "form-control"}


# Create your views here.
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
        return render(request, 'html/index/login.html')

    else:
        # 拿到登录的数据并进行校验
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 与数据库进行匹配
        user = m1.Users.objects.filter(name=username).first()
        if not user:
            # 匹配失败
            return render(request, 'html/index/login.html', {'username_error': "未找到用用户名"})

        if password != user.password:
            # 密码匹配失败
            return render(request, 'html/index/login.html', {'password_error': "密码匹配失败"})

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
        return render(request, 'html/index/register.html', {"form": form})
    else:
        data = user_form(request.POST, request.FILES)
        if data.is_valid():
            # 如果正确则保存
            data.save()
            # 返回login页面
            return redirect("../login")

        return render(request, 'html/index/register.html', {"form": data})


def index(request):
    '''
    req:
        ip/index
    res:
        get -> index.html  返回参数：{"ani_detail": data}
        get(search) -> search.html  返回参数：{"search_detail": data}
    '''

    if request.GET.get("search"):
        name = request.GET.get("search")
        data = m2.Anime_detail.objects.filter(name__iregex=r".*?{}.*?".format(name))
        if not data:
            nothing = "未找到相关结果，请重新提交"
        else:
            nothing = ''

        return render(request, "html/index/search.html",
                      {"search_detail": data, "search_name": name, "nothing": nothing})

    data = m2.Anime_detail.objects.all()
    return render(request, 'html/index/index.html', {"ani_detail": data})


def detail_page_default(request, num):
    '''
    当从首页跳转不带源编号时，默认跳转源1
    req:
        ip/index/(动漫编号[限制数字int])
            num -> 项目编号
    '''
    return redirect("./{}".format(1))


def detail_page(request, num, source):
    '''
    req:
        ip/index/(动漫编号[限制数字int])/(动漫编号[source])
            num -> 动漫编号
            source -> 源编号
    res：
        get(num) -> detail_page.html(这个是模板，内容根据num值添加)   参数：{"ani_detail": data, "episodes": episodes,
                                                                        "source": source_data, "now_source": source}
    '''

    data = m2.Anime_detail.objects.get(store_number=num)
    episodes = data.episode_detail.all().filter(source_num=source)
    return render(request, 'html/index/Detail_page.html',
                  {"ani_data": data, "now_source": source, "episodes": episodes})


def video_page(request, num, source):
    '''
    req:
        ip/index/(动漫编号[num])/(动漫编号[source])/video?episode=...
            num     -> 动漫编号
            episode -> 现在是第几集
    res:
        get -> video_page.html      参数：{"ani_data"(详情页表对象): data,
                                          "episodes(此动漫集数所有表对象)": episodes,
                                          "now_episode"(当前集数对象): now_episode}
    '''
    # 拿到参数
    episode = request.GET.get("episode")

    # 拿到此视频的视频详情页的表
    data = m2.Anime_detail.objects.get(store_number=num)
    # 拿到集数的表
    eps_data = data.episode_detail.all()

    if source == 1:
        '''源1的解析'''
        # 拿到此视频具体集数表
        episodes = eps_data.filter(source_num=1)
        # 拿到现在的集数的url
        now_episode = episodes.get(episode=episode)
        now_episode_url = yinghua.get_url(url=now_episode.episode_url)
    return render(request, 'html/index/video_page.html',
                  {"ani_data": data, "episodes": episodes, "now_episode": now_episode,
                   "now_url": now_episode_url})


def clear(request):
    '''
    清除专用,用于清除session
    req:
        ip/index/clear
    '''
    request.session.clear()
    return redirect("/index/login")
