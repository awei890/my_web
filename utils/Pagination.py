def page_navigation(page, total, length):
    '''
    分页函数 （已经默认page <= total）
    page:当前页数
    total:展示数据需要几页
    length:分页栏长度，需要单数

    返回：data: 页面列表，用于前端循环
         i:游标，得到目前page在集合的第几个
    '''
    if page > total:
        # 保证当前数不会超过总数
        return
    if not length % 2:
        # 保证是单数
        return

    # 总长度 > 分页长度
    if total > length:
        # 当前页数 > 分页长度中间数(左边)
        if page >= length // 2 + 1:
            # 当前页数 <= 总长度-分页长度中间数（右边）
            if page <= total - length // 2:
                data = [i for i in range(page - length // 2, page + length // 2 + 1)]
            else:
                data = [i + 1 for i in range(total - length, total)]

        # 当前页数 < 分页长度中间数(左边)
        if page < length // 2 + 1:
            data = [i + 1 for i in range(length)]

    # 总长度 < 分页长度
    else:
        data = [i + 1 for i in range(total)]

    # 拿到游标
    i = data.index(page)
    return data, i
