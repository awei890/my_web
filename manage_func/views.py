import os

from basic_func import models as m1
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from manage_func import models
from static.plugins.image_processing import pillow_process


# Create your views here.

class Detail_form(ModelForm):
    '''modelform插件，用于detail_edit'''

    class Meta:
        # 表是Anime_detail
        model = models.Anime_detail
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "status":
                field.widget.attrs = {"style": "width:15px; height:15px; padding-top:10px;"}
            elif name == "introduction":
                field.widget.attrs = {"class": "form-control", "rows": "5"}
            # elif name == "image":
            #     field.widget.attrs = {}
            else:
                field.widget.attrs = {"class": "form-control"}


class Source_form(ModelForm):
    '''modelform插件，用于episode_edit'''

    class Meta:
        # 表是Anime_source
        model = models.Anime_source
        fields = "__all__"
        exclude = ["link"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


class Episode_form(ModelForm):
    '''modelform插件，用于episode_edit'''

    class Meta:
        # 表是Anime_episode
        model = models.Anime_episode
        fields = "__all__"
        exclude = ["link"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


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


class Manager_form(ModelForm):
    '''modelform插件，用于管理员系统'''

    class Meta:
        # 表是Manager
        model = models.Manager
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def detail(request):
    '''
    动漫详情页管理
    req:
        ip/manage/detail
    res:
        get                                         -> ani_detail.html            参数：{'ani_data': ani_data}
        get(add)                                    -> ani_add.html               参数：{"form": detail_form}
        get(edit and num[视频编号])                   -> ani_edit.html             参数：{"form": ani_data})
        get(delete and num[视频编号])                 -> 删除数据，返回                    {"delete": True}

        post(由ani_add.html提交表单而来)(save)         ->   ip/manage/detail(重定向)
        post(由ani_re_edit.html提交表单而来)(re_edit)  ->   ip/manage/detail(重定向)

    '''

    if request.method == "GET":
        if request.GET.get("add"):
            # 添加详情页面
            detail_form = Detail_form()
            return render(request, 'html/manage/ani_manage/ani_add.html', {"form": detail_form})

        if request.GET.get("edit"):
            # 编辑详情页数据
            num = request.GET.get("num")
            o = models.Anime_detail.objects.get(store_number=num)
            ani_data = Detail_form(instance=o)
            return render(request, 'html/manage/ani_manage/ani_re_edit.html', {"form": ani_data})

        if request.GET.get("delete") and request.GET.get("num"):
            # 删除操作
            num = request.GET.get("num")
            models.Anime_detail.objects.filter(store_number=num).first().delete()
            # 返回一个json文件表示删除完成
            return JsonResponse({"delete": True})

        ani_data = models.Anime_detail.objects.all()
        return render(request, 'html/manage/ani_manage/ani_detail.html', {'ani_data': ani_data})

    # +++-----------------------------------上面为get请求，下面为post请求---------------------------------------------+++

    if request.method == 'POST':
        if request.POST.get("save"):
            # 这个是详情页提交表单
            data = Detail_form(request.POST, request.FILES)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./detail")

            # 否则返回错误信息
            return render(request, 'html/manage/ani_manage/ani_add.html', {"form": data})

        if request.POST.get("re_edit"):

            # 这个是重新编写详情
            num = request.POST.get("store_number")
            # 拿到对象
            o = models.Anime_detail.objects.get(store_number=num)
            # 拿到源文件图片路径（用于后面删除）
            image_path = o.image
            # 拿到数据重新覆盖对象
            data = Detail_form(request.POST, request.FILES, instance=o)

            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 如果源路径存在图片  and  后来的路径与源路径不同
                if o.image != "{}".format(image_path) and os.path.exists("{}".format(image_path)):
                    # 删除原图片
                    os.remove("{}".format(image_path))
                # 图片处理(图片原路径覆盖)
                pillow_process.Image_process("{}".format(o.image), width=240)
                # 返回detail页面
                return redirect("./detail")

            # 否则返回错误信息
            return render(request, 'html/manage/ani_manage/ani_re_edit.html', {"form": data})


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————

def source(request, num):
    '''
    动漫源管理
    req:
        ip/manage/detail/<int:num>
    res:
        get -> source_detail.html         参数：{"source_list": data}
        get(add)  ->  source_add.html     参数：{"form": form}
        get(edit) ->  source_edit.html    参数：{"form": instance}
        get(delete)  ->  返回参数               {"form": instance}

         post(由source_add.html提交表单而来)(save)        ->      ip/manage/detail/(num视频储藏号)(重定向)
        post(由source_edit.html提交表单而来)(re_edit)  ->      ip/manage/detail/(num视频储藏号)(重定向)
    '''

    # 详情页
    now_ani = models.Anime_detail.objects.filter(store_number=num).first()

    if request.method == "GET":
        if request.GET.get("add"):
            # 进入添加页面
            form = Source_form()
            return render(request, 'html/manage/source_manage/source_add.html', {"form": form})

        if request.GET.get("edit"):
            # 进入编辑页面
            source_num = request.GET.get("source_num")
            o = now_ani.Anime_source.all().filter(source_num=source_num).first()
            instance = Source_form(instance=o)
            return render(request, "html/manage/source_manage/source_edit.html", {"form": instance})

        if request.GET.get("delete"):
            # 删除
            name = request.GET.get("name")
            now_ani.Anime_source.all().filter(name=name).first().delete()
            # 返回一个json文件表示删除完成
            return JsonResponse({"delete": True})

        # 整体展示页面
        data = now_ani.Anime_source.all()
        return render(request, 'html/manage/source_manage/source_detail.html', {"source_list": data, "num": num})

    else:
        # 添加的表单
        if request.POST.get("save"):
            # 这个是提交表单
            data = Source_form(request.POST, request.FILES)
            # 设置默认外键链接(instance表示现在)
            data.instance.link = now_ani

            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回集数展示页面
                return redirect("./{}".format(num))

            # 否则返回错误信息
            return render(request, 'html/manage/source_manage/source_edit.html', {"form": data})

        if request.POST.get("re_edit"):
            # 重新编辑表单
            name = request.POST.get("name")
            # 这个是重新编写详情
            o = now_ani.Anime_source.all().filter(name=name).first()
            # 拿到数据重新覆盖对象
            data = Source_form(request.POST, request.FILES, instance=o)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./{}".format(num))

            # 否则返回错误信息
            return render(request, 'html/manage/source_manage/source_edit.html',
                          {"form": data})


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def episode(request, num, source):
    '''
    动漫集数管理
    req:
        ip/manage/detail/<int:num>/<int:source>
    res:
        get                 -> episode_detail.html              参数：{"epi_list": episode_list, "num": num}
        get(add)            -> episode_edit.html                参数：{"form": episode_form, "num": num}
        get(edit)           -> episode_re_edit.html             参数：{"form": ani_data, "mysql_id": mysql_id, "num": num}
        get(delete)         -> 返回参数                          参数：{"delete": True}

        post(由episode_edit.html提交表单而来)(save)        ->      ip/manage/detail/(num视频储藏号)(重定向)
        post(由episode_re_edit.html提交表单而来)(re_edit)  ->      ip/manage/detail/(num视频储藏号)(重定向)
    '''
    # 先找到详情页，再通过外键找到他的当前源对象
    now_source = models.Anime_detail.objects.get(store_number=num).Anime_source.get(source_num=source)

    if request.method == 'GET':
        if request.GET.get("add"):
            # 这个是添加视频集数
            episode_form = Episode_form()
            return render(request, 'html/manage/episode_manage/episode_edit.html', {"form": episode_form, "num": num})

        if request.GET.get("edit"):
            mysql_id = request.GET.get("mysql_id")
            # 编辑视频集数数据
            o = now_source.episode_detail.all().get(id=mysql_id)
            ani_data = Episode_form(instance=o)
            return render(request, 'html/manage/episode_manage/episode_re_edit.html',
                          {"form": ani_data, "mysql_id": mysql_id, "num": num})

        if request.GET.get("delete"):
            mysql_id = request.GET.get("mysql_id")
            # 删除操作
            # 这里由动漫主页面通过外键拿到所有集数对象
            epi_list = now_source.episode_detail.all()
            # 集数删除
            epi_list.get(id=mysql_id).delete()
            # 返回一个json文件表示删除完成
            return JsonResponse({"delete": True})

        # 先找到详情页，再通过外键找到他的所有源，再找他所有的集数
        episode_list = now_source.episode_detail.all()
        return render(request, 'html/manage/episode_manage/episode_detail.html', {"epi_list": episode_list, "num": num})

    # +++-----------------------------------上面为get请求，下面为post请求------------------------------------------------+++

    if request.method == 'POST':
        if request.POST.get("save"):
            # 这个是提交表单
            data = Episode_form(request.POST, request.FILES)
            # 设置默认外键链接(instance表示现在)
            data.instance.link = now_source

            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回集数展示页面
                return redirect("./{}".format(source))

            # 否则返回错误信息
            return render(request, 'html/manage/episode_manage/episode_edit.html',
                          {"form": data, "num": num})

        if request.POST.get("re_edit"):
            # 这个是重新编写详情
            mysql_id = request.POST.get("mysql_id")
            # 拿到对象
            o = now_source.episode_detail.all().get(id=mysql_id)
            # 拿到数据重新覆盖对象
            data = Episode_form(request.POST, request.FILES, instance=o)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./{}".format(source))

            # 否则返回错误信息
            return render(request, 'html/manage/episode_manage/episode_re_edit.html',
                          {"form": data, "mysql_id": mysql_id, "num": num})


# 动漫页管理
# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
# 用户或管理员账号管理
def manage(request):
    '''
    管理页面详情页
    req:
        ip/manage
    res:
        get -> manage_index.html
    '''
    return render(request, "html/manage/manage_index.html")


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def users(request):
    '''
    用户管理详情页
    req:
        ip/manage/user
    res:
        get                 -> user_detail.html
        get(delete)         -> 返回参数                          参数：{"delete": True}
        get(edit)           -> 返回参数                          参数：{"form": form}
        get(add)            -> user_add.html                    参数：{"form": form}

        post(由user_re_edit.html提交表单而来)(re_edit)   ->      ip/manage/users(重定向)
    '''
    if request.method == "GET":
        if request.GET.get("add"):
            # 这个是添加视频集数
            form = user_form()
            return render(request, 'html/manage/users_manage/user_add.html', {"form": form})

        if request.GET.get("delete"):
            # 拿到参数，用户名
            name = request.GET.get("name")
            # 根据用户名删除数据库中的表
            m1.Users.objects.get(name=name).delete()
            # 返回已删除的信号
            return JsonResponse({"delete": True})

        if request.GET.get("edit"):
            # 拿到参数，用户名
            name = request.GET.get("name")
            # 根据用户名拿到对象
            user = m1.Users.objects.get(name=name)
            # 用modelform插件传过去对象
            form = user_form(instance=user)
            return render(request, "html/manage/users_manage/user_re_edit.html", {"form": form})

        o = m1.Users.objects.all()
        return render(request, "html/manage/users_manage/user_detail.html", {"form": o})

    else:
        if request.POST.get("save"):
            # modelform拿到传来的数据
            data = user_form(request.POST, request.FILES)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回user页面
                return redirect("./users")
            # 否则返回错误信息
            return render(request, 'html/manage/users_manage/user_add.html', {"form": data})

        if request.POST.get("re_edit"):
            # 拿到用户名
            name = request.POST.get("name")
            # 数据库比对用户名
            o = m1.Users.objects.get(name=name)
            # 拿到源文件图片路径（用于后面删除）
            image_path = o.user_image
            # modelform拿到传来的数据
            data = user_form(request.POST, request.FILES, instance=o)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 如果源路径存在图片  并且  后来的路径 与 源路径不同
                if o.user_image != "{}".format(image_path) and os.path.exists("{}".format(image_path)):
                    # 删除原图片
                    os.remove("{}".format(image_path))
                # 返回user页面
                return redirect("./users")

            # 否则返回错误信息
            return render(request, "html/manage/users_manage/user_re_edit.html", {"form": data})


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def login(request):
    '''
    管理员用户登录
    req:
        ip/manage/login
    req:
        get ->  manage_login.html

        post ->
    '''
    if request.method == "GET":
        return render(request, "html/manage/manage_login.html")

    else:
        # 拿到数据
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        root = models.Manager.objects.filter(name=name).first()

        if not root:
            # 是否存在
            return HttpResponse("用户不存在")

        if pwd != root.password:
            # 密码是否匹配
            return HttpResponse("密码错误")

        request.session["manage_info"] = {"username": name, "password": pwd}
        return redirect("/manage")


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def manager_list(request):
    '''
    管理员列表
    req
        ip/manage/administrators
    res
        get         ->      manager_list.html
        get(delete) ->                                  {"delete": True}
        get(add)    ->      manager_add.html            {"form": form}
        get(edit)   ->      manager_re_edit.html        {"data": data}

        post(由manager_add.html提交表单而来)(save)         ->    重定向  ip/manage/administrators
        post(由manager_re_edit.html提交表单而来)(re_edit)  ->    重定向  同上
    '''
    if request.method == "GET":

        if request.GET.get("delete"):
            # 这是删除
            name = request.GET.get("name")
            manager = models.Manager.objects.filter(name=name).first()
            manager.delete()
            return JsonResponse({"delete": True})

        if request.GET.get('add'):
            # 这是添加
            form = Manager_form()
            return render(request, "html/manage/manage_list/manager_add.html", {"form": form})

        if request.GET.get("edit"):
            # 这是编辑
            name = request.GET.get("name")
            now_manager = models.Manager.objects.filter(name=name).first()
            data = Manager_form(instance=now_manager)
            return render(request, "html/manage/manage_list/manager_re_edit.html", {"data": data})

        data = models.Manager.objects.all()
        return render(request, "html/manage/manage_list/manager_list.html", {"data": data})

    else:
        if request.POST.get("save"):
            # 这是添加提交的订单
            data = Manager_form(request.POST, request.FILES)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./administrators")

            # 否则返回错误信息
            return render(request, "html/manage/manage_list/manager_add.html", {"form": data})

        if request.POST.get("re_edit"):
            # 这个是重新编写详情
            name = request.POST.get("name")
            # 拿到对象
            o = models.Manager.objects.filter(name=name).first()
            # 拿到数据重新覆盖对象
            data = Manager_form(request.POST, request.FILES, instance=o)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./administrators")

            # 否则返回错误信息
            return render(request, "html/manage/manage_list/manager_re_edit.html", {"data": data})


# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
def clear(request):
    '''清除专用'''
    request.session.clear()
    return redirect("/manage/login")


# 用户和管理员账号管理
# —————————————————————————————————————————————————————分割符————————————————————————————————————————————————————————————
# 博客系统

class Channel_form(ModelForm):
    """ 用于展示channel频道 """

    class Meta:
        model = models.Channel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "image":
                field.widget.attrs = {}
                continue
            field.widget.attrs = {"class": "form-control"}


def Channel_manage(request):
    """
    频道管理
    req:
        ip/manage/channel
    res:
        get  ->  channel_detail.html
        get(add)  ->
    """
    if request.method == "GET":
        if request.GET.get("add"):
            # 这是添加
            form = Channel_form()
            return render(request, "html/manage/channel_manage/channel_add.html", {"form": form})

        form = models.Channel.objects.all()
        return render(request, 'html/manage/channel_manage/channel_detail.html', {"form": form})

    else:
        if request.POST.get("save"):
            # 这个是详情页提交表单
            data = Channel_form(request.POST, request.FILES)
            if data.is_valid():
                # 如果正确则保存
                data.save()
                # 返回detail页面
                return redirect("./channel")

            # 否则返回错误信息
            return render(request, "html/manage/channel_manage/channel_add.html", {"form": data})
