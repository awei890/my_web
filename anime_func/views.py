import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from anime_func import models
from anime_func.utils import yinghua
from django.db.models import Q


def index(request):
    '''
    req:
        ip/anime
    res:
        get -> ani_index.html  返回参数：{"ani_detail": data}
        get(search) -> search.html  返回参数：{"search_detail": data}
    '''

    if request.GET.get("search"):
        name = request.GET.get("search")
        data = models.Anime_detail.objects.filter(name__iregex=r".*?{}.*?".format(name))
        if not data:
            nothing = "未找到相关结果，请重新提交"
        else:
            nothing = ''

        return render(request, "./search.html",
                      {"search_detail": data, "search_name": name, "nothing": nothing})

    # 拿到week_tags的星期一到星期天
    update_anime = models.week_tags.objects.filter(~Q(week="0"))  # 反向过滤week=0，即week不等于0的
    # 创建一个字典储存数据
    json_data = dict()

    for index, item in enumerate(update_anime):
        # 循环加入星期一到星期天 每天所有的动漫对象
        json_data["week{}".format(index + 1)] = item.animes.all()

    # 动漫列表展示的数据
    data = models.Anime_detail.objects.all()
    # 随机抽取12个动漫进行展示
    choice_num = [random.randint(1, data.count()) for i in range(12)]
    json_data["ani_detail"] = data.filter(id__in=choice_num)
    return render(request, './ani_index.html', json_data)


def detail_page_default(request, num):
    '''
    当从首页跳转不带源编号时，默认跳转源1
    req:
        ip/index/(动漫编号[限制数字int])
            num -> 项目编号
    '''
    return redirect("./{}/{}".format(num, 1))


def detail_page(request, num, source):
    '''
    req:
        ip/anime/(动漫编号[限制数字int])/(动漫编号[source])
            num -> 动漫编号
            source -> 源编号
    res：
        get(num) -> detail_page.html(这个是模板，内容根据num值添加)   参数：{"ani_detail": data, "episodes": episodes,
                                                                        "source": source_data, "now_source": source}
    '''

    data = models.Anime_detail.objects.get(store_number=num)
    episodes = data.episode_detail.all().filter(source_num=source)
    return render(request, './detail_page.html',
                  {"ani_data": data, "now_source": source, "episodes": episodes})


def video_page(request, num, source):
    '''
    req:
        ip/anime/(动漫编号[num])/(动漫编号[source])/video?episode=...
            num     -> 动漫编号
            episode -> 现在是第几集
    res:
        get -> video_page.html      参数：{"ani_data"(详情页表对象): data,
                                          "episodes(此动漫集数所有表对象)": episodes,
                                          "now_episode"(当前集数对象): now_episode,
                                          "now_url"(video的url): url}
    '''
    # 拿到参数
    episode = request.GET.get("episode")

    # 拿到此视频的视频详情页的表
    data = models.Anime_detail.objects.get(store_number=num)
    # 拿到集数的表
    eps_data = data.episode_detail.all()

    if source == 1:
        '''源1的解析'''
        # 拿到此视频具体集数表
        episodes = eps_data.filter(source_num=1)
        # 拿到现在的集数的url
        now_episode = episodes.get(episode=episode)
        now_episode_url = yinghua.get_url(url=now_episode.episode_url)
    return render(request, './video_page.html',
                  {"ani_data": data, "episodes": episodes, "now_episode": now_episode,
                   "now_url": now_episode_url})
